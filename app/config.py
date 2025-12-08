from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Smart Energy Meter Backend"
    DATABASE_URL: str = "sqlite:///./energy_meter.db"
    MQTT_BROKER: str = "broker.hivemq.com"  # Public broker for testing, or localhost
    MQTT_PORT: int = 1883
    MQTT_TOPIC: str = "sensor/energy"
    GROQ_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
