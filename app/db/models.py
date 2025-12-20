from sqlalchemy import Column, Integer, String, Float, DateTime
from app.db.database import Base
from datetime import datetime

class Reading(Base):
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True, index=True)
    device = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    current = Column(Float)
    voltage = Column(Float)

class Device(Base):
    __tablename__ = "devices"

    id = Column(String, primary_key=True, index=True) # Device name acts as ID
    threshold = Column(Float, default=0.0)

