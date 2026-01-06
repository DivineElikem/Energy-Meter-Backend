import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Reading, Device, Base
from app.config import settings

def migrate_data(sqlite_url: str, postgres_url: str):
    """Migrates data from SQLite to PostgreSQL."""
    print(f"🚀 Starting migration...")
    print(f"Source: {sqlite_url}")
    print(f"Destination: {postgres_url}")

    # Connect to SQLite
    sqlite_engine = create_engine(sqlite_url)
    SqliteSession = sessionmaker(bind=sqlite_engine)
    sqlite_session = SqliteSession()

    # Connect to PostgreSQL
    pg_engine = create_engine(postgres_url)
    PgSession = sessionmaker(bind=pg_engine)
    pg_session = PgSession()

    # Create tables in Postgres if they don't exist
    Base.metadata.create_all(pg_engine)

    try:
        # 1. Migrate Devices
        devices = sqlite_session.query(Device).all()
        print(f"📦 Migrating {len(devices)} devices...")
        for dev in devices:
            # Check if device already exists to avoid duplicates
            if not pg_session.query(Device).filter_by(id=dev.id).first():
                pg_session.merge(dev)
        
        pg_session.commit()

        # 2. Migrate Readings
        readings = sqlite_session.query(Reading).all()
        print(f"📈 Migrating {len(readings)} readings...")
        for r in readings:
            # Check if reading already exists (optional but safer)
            pg_session.merge(r)
        
        pg_session.commit()
        print("✅ Migration completed successfully!")

    except Exception as e:
        pg_session.rollback()
        print(f"❌ Migration failed: {e}")
    finally:
        sqlite_session.close()
        pg_session.close()

if __name__ == "__main__":
    # Get local SQLite path
    local_sqlite = "sqlite:///./energy_meter.db"
    
    # Get Postgres URL from environment or prompt
    remote_pg = os.getenv("DATABASE_URL")
    
    if not remote_pg or remote_pg.startswith("sqlite"):
        print("⚠️  DATABASE_URL environment variable is not set to a PostgreSQL connection string.")
        remote_pg = input("Please enter your Render PostgreSQL External Connection String: ").strip()

    if remote_pg:
        migrate_data(local_sqlite, remote_pg)
    else:
        print("Aborted.")
