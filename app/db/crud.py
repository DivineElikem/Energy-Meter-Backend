from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.db.models import Reading, Device
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

def get_device(db: Session, device_id: str):
    return db.query(Device).filter(Device.id == device_id).first()

def create_or_update_device(db: Session, device_id: str, threshold: float):
    db_device = get_device(db, device_id)
    if db_device:
        db_device.threshold = threshold
    else:
        db_device = Device(id=device_id, threshold=threshold)
        db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def get_anomalies(db: Session, device_id: str, limit: int = 100):
    """
    Get readings for a specific device that exceed its set threshold.
    Anomaly is defined here as (current * voltage) > threshold.
    If no threshold is set, we return an empty list or use a default if appropriate.
    """
    device = get_device(db, device_id)
    if not device or device.threshold <= 0:
        return []

    # Filtering for readings where power (current * voltage) > threshold
    return db.query(Reading).filter(
        Reading.device == device_id,
        (Reading.current * Reading.voltage) > device.threshold
    ).order_by(Reading.timestamp.desc()).limit(limit).all()

def get_all_devices(db: Session):
    # Get set thresholds
    set_thresholds = {d.id: d.threshold for d in db.query(Device).all()}
    
    # Get all unique device names from readings
    all_device_names = [r[0] for r in db.query(Reading.device).distinct().all()]
    
    results = []
    for name in all_device_names:
        results.append(Device(
            id=name,
            threshold=set_thresholds.get(name, 2500.0) # Default to 2500W
        ))
    return results

def get_recent_anomalies(db: Session, hours: int = 24):
    """Summarize anomalous activity across all devices in the last N hours."""
    since = datetime.now() - timedelta(hours=hours)
    
    # Get all devices to know their thresholds
    devices = db.query(Device).all()
    device_map = {d.id: d.threshold for d in devices}
    
    anomalies_summary = {}
    
    # We query readings since the time window
    readings = db.query(Reading).filter(Reading.timestamp >= since).all()
    
    for r in readings:
        threshold = device_map.get(r.device, 2500.0)
        power = r.voltage * r.current
        if power > threshold:
            if r.device not in anomalies_summary:
                anomalies_summary[r.device] = 0
            anomalies_summary[r.device] += 1
            
    return anomalies_summary




