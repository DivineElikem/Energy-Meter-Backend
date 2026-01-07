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

    # Connect to PostgreSQL with SSL required for Render
    # We also add pool_pre_ping to handle dropped connections better
    if "sslmode" not in postgres_url:
        separator = "&" if "?" in postgres_url else "?"
        postgres_url += f"{separator}sslmode=require"

    pg_engine = create_engine(
        postgres_url, 
        pool_pre_ping=True,
        connect_args={"sslmode": "require"}
    )
    PgSession = sessionmaker(bind=pg_engine)
    pg_session = PgSession()

    # Create tables in Postgres if they don't exist
    Base.metadata.create_all(pg_engine)

    try:
        # 1. Migrate Devices
        devices = sqlite_session.query(Device).all()
        print(f"📦 Migrating {len(devices)} devices...")
        for dev in devices:
            pg_session.merge(dev)
        pg_session.commit()

        # 2. Migrate Readings in Chunks
        total_readings = sqlite_session.query(Reading).count()
        print(f"📈 Migrating {total_readings} readings in batches of 500...")
        
        batch_size = 500
        count = 0
        
        while count < total_readings:
            # Fetch a chunk from SQLite
            chunk = sqlite_session.query(Reading).offset(count).limit(batch_size).all()
            
            for r in chunk:
                # Merge into Postgres
                pg_session.merge(r)
            
            pg_session.commit()
            count += len(chunk)
            print(f"✅ Progress: {count}/{total_readings} ({(count/total_readings)*100:.1f}%)")

        print("🎉 Migration completed successfully!")

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
