from pydantic import BaseModel
from datetime import datetime

class ReadingBase(BaseModel):
    device: str
    current: float
    voltage: float

class ReadingCreate(ReadingBase):
    timestamp: datetime

class Reading(ReadingBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
