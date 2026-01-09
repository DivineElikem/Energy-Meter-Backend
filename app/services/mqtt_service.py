import json
import paho.mqtt.client as mqtt
from sqlalchemy.orm import Session
from app.config import settings
from app.db.database import SessionLocal
from app.db.models import Reading
from datetime import datetime

def save_reading(payload: dict, db: Session):
    """Saves a reading to the database."""
    try:
        timestamp = datetime.fromisoformat(payload["timestamp"])
        reading = Reading(
            device=payload["device"],
            timestamp=timestamp,
            current=payload["current"],
            voltage=payload["voltage"]
        )
        db.add(reading)
        db.commit()
        db.refresh(reading)
        print(f"Saved reading for {reading.device} at {reading.timestamp}")
    except Exception as e:
        print(f"Error saving reading: {e}")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT Broker!")
        client.subscribe(settings.MQTT_TOPIC)
        print(f"📡 Subscribed to topic: {settings.MQTT_TOPIC}")
    else:
        print(f"❌ Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        payload_raw = msg.payload.decode()
        print(f"📩 Received message on {topic}: {payload_raw}")
        payload = json.loads(payload_raw)
        # Create a new database session for each message
        db = SessionLocal()
        try:
            save_reading(payload, db)
        finally:
            db.close()
    except Exception as e:
        print(f"⚠️ Error processing message: {e}")

from paho.mqtt.client import CallbackAPIVersion

mqtt_client = mqtt.Client(CallbackAPIVersion.VERSION1)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

def start_mqtt_listener():
    print(f"Connecting to MQTT Broker at {settings.MQTT_BROKER}...")
    try:
        mqtt_client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, 60)
        mqtt_client.loop_start()
    except Exception as e:
        print(f"Failed to start MQTT listener: {e}")

def stop_mqtt_listener():
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
