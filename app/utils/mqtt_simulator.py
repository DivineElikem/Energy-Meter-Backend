import time
import json
import random
import paho.mqtt.client as mqtt
from datetime import datetime

from app.config import settings
from app.utils.firebase_init import db_ref

# Configuration from app settings
BROKER = settings.MQTT_BROKER
PORT = settings.MQTT_PORT
TOPIC = settings.MQTT_TOPIC

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Simulator connected to MQTT Broker!")
    else:
        print(f"❌ Simulator failed to connect, return code {rc}")

from paho.mqtt.client import CallbackAPIVersion

def run_simulator():
    """Syncs data from Firebase RTD and publishes to MQTT."""
    client = mqtt.Client(CallbackAPIVersion.VERSION1)
    client.on_connect = on_connect

    print(f"Connecting to {BROKER}...")
    try:
        client.connect(BROKER, PORT, 60)
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    client.loop_start()

    try:
        while True:
            if not db_ref:
                print("⚠️ Firebase not initialized in simulator.")
                time.sleep(10)
                continue

            try:
                # Fetch current states and total consumption from Firebase
                snapshot = db_ref.reference("/").get()
                if not snapshot:
                    print("⚠️ No data in Firebase RTD.")
                    time.sleep(10)
                    continue

                total_voltage = snapshot.get("totalVoltage", 230.0)
                total_current = snapshot.get("totalCurrent", 0.0)
                relay1 = snapshot.get("relay1", False)
                relay2 = snapshot.get("relay2", False)

                # Estimate bulb consumption
                bulb1_current = round(random.uniform(0.052, 0.054), 3) if relay1 else 0.0
                bulb2_current = round(random.uniform(0.052, 0.054), 3) if relay2 else 0.0

                # Calculate combined sockets consumption
                # Ensures it doesn't go below 0 due to estimation errors
                sockets_current = max(0.0, round(total_current - (bulb1_current + bulb2_current), 3))

                # Prepare readings
                timestamp = datetime.utcnow().isoformat()
                
                readings = [
                    {"device": "bulb_1", "timestamp": timestamp, "current": bulb1_current, "voltage": total_voltage},
                    {"device": "bulb_2", "timestamp": timestamp, "current": bulb2_current, "voltage": total_voltage},
                    {"device": "sockets", "timestamp": timestamp, "current": sockets_current, "voltage": total_voltage},
                ]

                for reading in readings:
                    payload = json.dumps(reading)
                    client.publish(TOPIC, payload)
                    print(f"Published to {TOPIC}: {payload}")

            except Exception as e:
                print(f"Error fetching from Firebase: {e}")

            time.sleep(10) # Sync every 10 seconds
    except KeyboardInterrupt:
        print("Stopping sync...")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    run_simulator()
