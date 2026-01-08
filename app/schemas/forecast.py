from pydantic import BaseModel
from typing import List

class ForecastPoint(BaseModel):
    date: str
    predicted_energy: float

class ForecastResponse(BaseModel):
    forecast: List[ForecastPoint]
    outlook: str = ""
    tip: str = ""

