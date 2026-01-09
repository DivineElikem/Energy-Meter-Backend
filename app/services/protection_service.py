from sqlalchemy.orm import Session
from app.db import crud
from app.utils.firebase_init import db_ref

# DEVICE_TO_RELAY_MAP defines which Firebase relay(s) to turn off for each device
DEVICE_TO_RELAY_MAP = {
    "bulb_1": ["relay1"],
    "bulb_2": ["relay2"],
    "sockets": ["relay3", "relay4"]
}

def check_and_trigger_cutoff(payload: dict, db: Session):
    """
    Checks if a reading exceeds its device threshold and triggers off signal in Firebase.
    """
    try:
        device_id = payload.get("device")
        current = payload.get("current", 0)
        voltage = payload.get("voltage", 0)
        power = current * voltage

        if not device_id or power <= 0:
            return

        # Get device threshold from DB. Default to 2500W if not set.
        device_record = crud.get_device(db, device_id)
        threshold = device_record.threshold if device_record else 2500.0

        if power >= threshold:
            print(f"🚨 THRESHOLD EXCEEDED: {device_id} is consuming {power:.2f}W (Threshold: {threshold}W)")
            
            relays_to_cut = DEVICE_TO_RELAY_MAP.get(device_id, [])
            if not relays_to_cut:
                return

            if not db_ref:
                print("⚠️ Cannot trigger cut-off: Firebase not initialized.")
                return

            for relay in relays_to_cut:
                print(f"🔌 Turning OFF {relay} for safety...")
                db_ref.reference(relay).set(False)

    except Exception as e:
        print(f"⚠️ Error in protection logic: {e}")
