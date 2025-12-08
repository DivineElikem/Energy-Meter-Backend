from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config import settings
from app.api.endpoints import readings, analytics, forecast, chatbot, health
from app.services.mqtt_service import start_mqtt_listener, stop_mqtt_listener
from app.db.database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up...")
    Base.metadata.create_all(bind=engine)
    start_mqtt_listener()
    yield
    # Shutdown
    print("Shutting down...")
    stop_mqtt_listener()

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# Include routers
app.include_router(readings.router, prefix="/readings", tags=["Readings"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(forecast.router, prefix="/forecast", tags=["Forecast"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])
app.include_router(health.router, prefix="/health", tags=["Health"])

@app.get("/")
def root():
    return {"message": "Welcome to Smart Energy Meter Backend"}
