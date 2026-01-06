import time
import json
import random
import paho.mqtt.client as mqtt
from datetime import datetime

from app.config import settings

# Configuration from app settings
BROKER = settings.MQTT_BROKER
PORT = settings.MQTT_PORT
TOPIC = settings.MQTT_TOPIC

DEVICES = ["bulb_1", "bulb_2", "socket_1", "socket_2"]

def generate_reading(device):
    """Generates a realistic reading for a device."""
    if "bulb" in device:
        current = round(random.uniform(0.05, 0.15), 2)  # Low current for bulbs
    else:
        current = round(random.uniform(0.5, 2.5), 2)    # Higher current for sockets
    
    voltage = round(random.uniform(220.0, 240.0), 1)
    
    return {
        "device": device,
        "timestamp": datetime.utcnow().isoformat(),
        "current": current,
        "voltage": voltage
    }

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

def main():
    client = mqtt.Client()
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
            for device in DEVICES:
                reading = generate_reading(device)
                payload = json.dumps(reading)
                client.publish(TOPIC, payload)
                print(f"Published to {TOPIC}: {payload}")
            
            time.sleep(10) # Publish every 10 seconds
    except KeyboardInterrupt:
        print("Stopping simulator...")
        client.loop_stop()
        client.disconnect()

def run_simulator():
    """Starts the simulator in the current thread."""
    main()

if __name__ == "__main__":
    main()
