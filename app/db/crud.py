from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.db.models import Reading, Device
from datetime import datetime, timedelta, date

def get_readings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Reading).offset(skip).limit(limit).all()

def get_readings_by_device(db: Session, device: str, limit: int = 100):
    return db.query(Reading).filter(Reading.device == device).order_by(Reading.timestamp.desc()).limit(limit).all()

def get_latest_readings(db: Session):
    """Get the latest reading for each device with a fallback for empty states."""
    try:
        # 1. Try to get unique devices
        device_names = [r[0] for r in db.query(Reading.device).distinct().all()]
        
        if not device_names:
            # Fallback: if no distinct devices found, just get the last few readings to see if anything exists
            return db.query(Reading).order_by(Reading.timestamp.desc()).limit(10).all()
        
        latest_readings = []
        for device in device_names:
            latest = db.query(Reading).filter(Reading.device == device).order_by(Reading.timestamp.desc()).first()
            if latest:
                latest_readings.append(latest)
        return latest_readings
    except Exception as e:
        print(f"⚠️ Error in get_latest_readings: {e}")
        return []

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
    """Get all devices and their thresholds, combining existing device records with unique names from readings."""
    # 1. Get all unique device names from the database
    device_names_from_readings = [r[0] for r in db.query(Reading.device).distinct().all()]
    
    # 2. Get all defined devices from the devices table
    defined_devices = {d.id: d.threshold for d in db.query(Device).all()}
    
    # 3. Combine them
    all_names = set(device_names_from_readings).union(defined_devices.keys())
    
    # If no data at all, return dummy devices for initial UI state
    if not all_names:
        return [
            Device(id="bulb_1", threshold=2500.0),
            Device(id="bulb_2", threshold=2500.0),
            Device(id="socket_1", threshold=2500.0),
            Device(id="socket_2", threshold=2500.0),
        ]

    results = []
    for name in all_names:
        results.append(Device(
            id=name,
            threshold=defined_devices.get(name, 2500.0)
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

def get_power_trend(db: Session, window_minutes: int = 5):
    """Calculates the trend for power draw.
    Compares the average power of the last 'window' minutes with the average power of the 'window' minutes before that.
    """
    now = datetime.now()
    window_start = now - timedelta(minutes=window_minutes)
    previous_window_start = now - timedelta(minutes=window_minutes * 2)

    # Current window average power
    current_avg = db.query(func.avg(Reading.voltage * Reading.current)).filter(
        Reading.timestamp >= window_start,
        Reading.timestamp < now
    ).scalar() or 0.0

    # Previous window average power
    previous_avg = db.query(func.avg(Reading.voltage * Reading.current)).filter(
        Reading.timestamp >= previous_window_start,
        Reading.timestamp < window_start
    ).scalar() or 0.0

    if previous_avg == 0:
        return 0.0 # No trend possible without historical data
    
    trend_percentage = ((current_avg - previous_avg) / previous_avg) * 100
    return round(trend_percentage, 1)




