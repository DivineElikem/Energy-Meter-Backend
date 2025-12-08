from pydantic import BaseModel
from typing import List

class ForecastPoint(BaseModel):
    timestamp: str
    predicted_energy_kwh: float
    lower_bound: float
    upper_bound: float

class ForecastResponse(BaseModel):
    forecast: List[ForecastPoint]
