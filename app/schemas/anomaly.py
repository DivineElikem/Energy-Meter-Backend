from pydantic import BaseModel
from typing import List
from app.schemas.reading import Reading

class AnomalyResponse(BaseModel):
    device_id: str
    threshold: float
    anomalies: List[Reading]
