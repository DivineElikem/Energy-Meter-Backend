from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Smart Energy Meter Backend"
    DATABASE_URL: str = "sqlite:///./energy_meter.db"
    MQTT_BROKER: str = "broker.hivemq.com"  # Public broker for testing, or localhost
    MQTT_PORT: int = 1883
    MQTT_TOPIC: str = "sensor/energy"
    GROQ_API_KEY: str = ""
    START_SIMULATOR: bool = True
    FIREBASE_SERVICE_ACCOUNT: str = "app/utils/smart-energy-meter-4a732-firebase-adminsdk-fbsvc-dbd5bd6660.json"
    FIREBASE_SERVICE_ACCOUNT_JSON: str = "" # Full JSON string for production
    FIREBASE_DATABASE_URL: str = "https://smart-energy-meter-4a732-default-rtdb.firebaseio.com/"

    class Config:
        env_file = ".env"

settings = Settings()
