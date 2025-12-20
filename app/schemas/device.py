from pydantic import BaseModel

class DeviceBase(BaseModel):
    id: str
    threshold: float

class DeviceCreate(BaseModel):
    threshold: float

class Device(DeviceBase):
    class Config:
        from_attributes = True
