import pandas as pd
from prophet import Prophet
from sqlalchemy.orm import Session
from app.db.models import Reading
from datetime import datetime, timedelta

def generate_forecast(db: Session, days: int = 7):
    """Generates energy usage forecast for the next N days."""
    
    # Fetch all readings
    # In a real app, we might want to aggregate by hour or day first in SQL
    readings = db.query(Reading).all()
    
    if not readings:
        return {"message": "Not enough data to forecast"}

    data = []
    for r in readings:
        # Approximate energy (kWh) for this reading (assuming 10s interval)
        energy = (r.voltage * r.current * 10) / 3600000
        data.append({
            "ds": r.timestamp,
            "y": energy
        })
    
    df = pd.DataFrame(data)
    
    # Aggregate by minute to smooth out data and make Prophet faster (for testing)
    # In production, 'H' (hourly) or 'D' (daily) is better.
    df = df.set_index('ds').resample('min').sum().reset_index()
    
    # Rename columns for Prophet
    df.columns = ['ds', 'y']
    
    # Ensure we have enough data points
    if len(df) < 5: # Reduced for testing
         return {"message": "Not enough data points for reliable forecast (need > 5 minutes)"}

    m = Prophet()
    m.fit(df)
    
    future = m.make_future_dataframe(periods=days * 24, freq='H')
    forecast = m.predict(future)
    
    # Format results
    result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(days * 24)
    
    forecast_data = []
    for _, row in result.iterrows():
        forecast_data.append({
            "timestamp": row['ds'].isoformat(),
            "predicted_energy_kwh": round(max(0, row['yhat']), 6), # No negative energy
            "lower_bound": round(max(0, row['yhat_lower']), 6),
            "upper_bound": round(max(0, row['yhat_upper']), 6)
        })
        
    return forecast_data
