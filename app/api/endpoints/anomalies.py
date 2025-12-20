from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db import crud
from app.schemas.device import Device, DeviceCreate
from app.schemas.anomaly import AnomalyResponse

router = APIRouter()

@router.get("/devices", response_model=List[Device])
def read_all_devices(db: Session = Depends(get_db)):
    """Get all registered devices and their thresholds."""
    return crud.get_all_devices(db)

@router.post("/devices/{device_id}/threshold", response_model=Device)

def set_device_threshold(device_id: str, device_in: DeviceCreate, db: Session = Depends(get_db)):
    """Set or update the threshold for a specific device."""
    return crud.create_or_update_device(db, device_id=device_id, threshold=device_in.threshold)

@router.get("/devices/{device_id}/threshold", response_model=Device)
def read_device_threshold(device_id: str, db: Session = Depends(get_db)):
    """Get the current threshold for a specific device."""
    db_device = crud.get_device(db, device_id=device_id)
    if not db_device:
        return {"id": device_id, "threshold": 2500.0}
    return db_device


@router.get("/{device_id}", response_model=AnomalyResponse)
def get_device_anomalies(device_id: str, limit: int = 100, db: Session = Depends(get_db)):
    """Get recent readings that exceed the device's threshold."""
    db_device = crud.get_device(db, device_id=device_id)
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found or no threshold set")
    
    anomalies = crud.get_anomalies(db, device_id=device_id, limit=limit)
    return {
        "device_id": device_id,
        "threshold": db_device.threshold,
        "anomalies": anomalies
    }
