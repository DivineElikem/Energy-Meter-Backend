from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.firebase_init import db_ref

router = APIRouter()

class DeviceState(BaseModel):
    state: bool

@router.get("/")
def get_device_states():
    try:
        if not db_ref:
            raise HTTPException(status_code=500, detail="Firebase not initialized")
        
        # We need to fetch the root or specific relay keys
        # Based on user input: relay1, relay2, relay3, relay4
        # We'll fetch the entire root for now or specific keys if preferred.
        # Let's fetch one by one to ensure we get exactly what we need if root is messy.
        
        relays = ["relay1", "relay2", "relay3", "relay4"]
        states = {}
        for r in relays:
            val = db_ref.reference(r).get()
            states[r] = val if val is not None else False # Default to false if not set
            
        return states
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{relay_id}")
def update_device_state(relay_id: str, device_state: DeviceState):
    try:
        if not db_ref:
            raise HTTPException(status_code=500, detail="Firebase not initialized")
        
        if relay_id not in ["relay1", "relay2", "relay3", "relay4"]:
            raise HTTPException(status_code=400, detail="Invalid relay ID")
            
        db_ref.reference(relay_id).set(device_state.state)
        return {"relay_id": relay_id, "state": device_state.state}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
