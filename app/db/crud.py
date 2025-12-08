from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.db.models import Reading
from datetime import datetime, timedelta, date

def get_readings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Reading).offset(skip).limit(limit).all()

def get_readings_by_device(db: Session, device: str, limit: int = 100):
    return db.query(Reading).filter(Reading.device == device).order_by(Reading.timestamp.desc()).limit(limit).all()

def get_latest_readings(db: Session):
    """Get the latest reading for each device."""
    subquery = db.query(
        Reading.device,
        func.max(Reading.timestamp).label('max_timestamp')
    ).group_by(Reading.device).subquery()

    return db.query(Reading).join(
        subquery,
        (Reading.device == subquery.c.device) & (Reading.timestamp == subquery.c.max_timestamp)
    ).all()

def get_daily_usage(db: Session, date_val: datetime | date):
    """Calculate total energy usage per device for a specific day."""
    # Energy (kWh) = (Voltage * Current * Time) / 1000
    # Since we have readings every 10 seconds, we can approximate.
    # Or simply sum (Voltage * Current) and assume a time interval.
    # For simplicity, let's just sum (Current * Voltage) for now as a proxy for "Instantaneous Power Sum"
    # To get actual energy, we'd need to integrate over time.
    # Let's assume each reading represents 10 seconds of usage.
    # Energy (Ws) = Power (W) * 10 (s)
    # Energy (kWh) = Power (W) * 10 (s) / (3600 * 1000)
    
    if isinstance(date_val, datetime):
        start_of_day = date_val.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        start_of_day = datetime.combine(date_val, datetime.min.time())
        
    end_of_day = start_of_day + timedelta(days=1)

    readings = db.query(Reading).filter(
        Reading.timestamp >= start_of_day,
        Reading.timestamp < end_of_day
    ).all()

    device_stats = {}
    for r in readings:
        if r.device not in device_stats:
            device_stats[r.device] = {"total_power": 0, "count": 0, "total_voltage": 0, "total_current": 0}
        
        power = r.voltage * r.current
        device_stats[r.device]["total_power"] += power
        device_stats[r.device]["total_voltage"] += r.voltage
        device_stats[r.device]["total_current"] += r.current
        device_stats[r.device]["count"] += 1

    results = []
    for device, stats in device_stats.items():
        # Energy in kWh: Total Power (W) * 10s / 3,600,000
        energy_kwh = (stats["total_power"] * 10) / 3600000
        avg_voltage = stats["total_voltage"] / stats["count"]
        avg_current = stats["total_current"] / stats["count"]
        
        results.append({
            "device": device,
            "total_energy": round(energy_kwh, 6),
            "avg_voltage": round(avg_voltage, 2),
            "avg_current": round(avg_current, 2)
        })
    
    return results
