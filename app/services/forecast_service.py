from sqlalchemy import func
from datetime import datetime, timedelta
import pandas as pd
from prophet import Prophet
from sqlalchemy.orm import Session
from app.db.models import Reading

def generate_forecast(db: Session, days: int = 7):
    """Generates energy usage forecast for the next N days using hourly aggregation."""
    
    # Efficiently aggregate energy by hour in SQL
    # Power (W) = V * I. Energy (Wh) = W * (hours). 
    # Since readings are roughly every 10s (1/360 hours), weight is 1/360.
    # To get kWh, divide by 1000. Total factor: 1/360000.
    
    # SQLite doesn't have date_trunc, so we use strftime
    hourly_readings = db.query(
        func.strftime('%Y-%m-%dT%H:00:00', Reading.timestamp).label('hour'),
        func.sum(Reading.voltage * Reading.current * 10 / 3600000).label('energy_kwh')
    ).group_by('hour').all()
    
    if not hourly_readings or len(hourly_readings) < 5:
        return {"message": "Not enough data points for reliable forecast"}

    data = [{"ds": r.hour, "y": r.energy_kwh} for r in hourly_readings]
    df = pd.DataFrame(data)
    df['ds'] = pd.to_datetime(df['ds'])

    m = Prophet(interval_width=0.95, yearly_seasonality=False, weekly_seasonality=True, daily_seasonality=True)
    m.fit(df)
    
    future = m.make_future_dataframe(periods=days * 24, freq='H')
    forecast = m.predict(future)
    
    result = forecast[['ds', 'yhat']].tail(days * 24)
    
    forecast_data = []
    for _, row in result.iterrows():
        # Align with frontend expectations: 'date' and 'predicted_energy'
        forecast_data.append({
            "date": row['ds'].strftime('%Y-%m-%d %H:%M'),
            "predicted_energy": round(max(0, row['yhat']), 4)
        })
        
    return forecast_data

