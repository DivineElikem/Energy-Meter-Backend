from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.forecast_service import generate_forecast
from app.schemas.forecast import ForecastResponse

router = APIRouter()

@router.post("/", response_model=ForecastResponse)
def get_energy_forecast(
    days: int = Query(default=7, ge=1, le=30),
    db: Session = Depends(get_db)
):
    forecast_data = generate_forecast(db, days)
    
    if isinstance(forecast_data, dict) and "message" in forecast_data:
        # Handle error case (not enough data)
        # For now, return empty list or raise HTTP exception. 
        # Let's return empty list to match schema, but maybe with a warning log.
        return {"forecast": []}

    return {"forecast": forecast_data}
