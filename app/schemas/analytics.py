from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class DeviceStats(BaseModel):
    device: str
    total_energy: float
    avg_voltage: float
    avg_current: float

class DailySummary(BaseModel):
    date: str
    total_energy: float
    power_trend: float = 0.0
    device_breakdown: List[DeviceStats]
