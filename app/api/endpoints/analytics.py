from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, date
from app.db.database import get_db
from app.db import crud
from app.schemas.analytics import DailySummary

router = APIRouter()

@router.get("/daily-summary", response_model=DailySummary)
def get_daily_summary(
    day: date = Query(default=date.today(), description="Date to retrieve summary for"),
    db: Session = Depends(get_db)
):
    # Convert date to datetime
    dt = datetime.combine(day, datetime.min.time())
    
    device_stats = crud.get_daily_usage(db, dt)
    total_energy = sum(d["total_energy"] for d in device_stats)
    
    # Calculate power trend (percentage)
    power_trend = crud.get_power_trend(db)
    
    return {
        "date": day.isoformat(),
        "total_energy": round(total_energy, 6),
        "power_trend": power_trend,
        "device_breakdown": device_stats
    }

@router.get("/highest-consumer")
def get_highest_consumer(
    day: date = Query(default=date.today(), description="Date to check"),
    db: Session = Depends(get_db)
):
    dt = datetime.combine(day, datetime.min.time())
    device_stats = crud.get_daily_usage(db, dt)
    
    if not device_stats:
        return {"message": "No data for this date"}
        
    highest = max(device_stats, key=lambda x: x["total_energy"])
    
    return {
        "date": day.isoformat(),
        "highest_consumer": highest
    }
