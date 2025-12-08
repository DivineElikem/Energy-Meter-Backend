from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db import crud
from app.schemas.reading import Reading

router = APIRouter()

@router.get("/latest", response_model=List[Reading])
def read_latest_readings(db: Session = Depends(get_db)):
    return crud.get_latest_readings(db)

@router.get("/device/{device_id}", response_model=List[Reading])
def read_device_readings(device_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    readings = crud.get_readings_by_device(db, device=device_id, limit=limit)
    if not readings:
        raise HTTPException(status_code=404, detail="Device not found or no readings")
    return readings

@router.get("/all", response_model=List[Reading])
def read_all_readings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_readings(db, skip=skip, limit=limit)
