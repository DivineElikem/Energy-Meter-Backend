import os
import threading
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Reading, Device, Base
from app.config import settings

def run_auto_migration():
    """Checks for local SQLite DB and migrates to Postgres if it exists."""
    sqlite_path = "energy_meter.db"
    
    if not os.path.exists(sqlite_path):
        return

    # Don't migrate if we are already using SQLite in production
    if settings.DATABASE_URL.startswith("sqlite"):
        return

    print("🔄 Found local SQLite database. Starting auto-migration to PostgreSQL...")
    
    def migrate():
        try:
            # Source (SQLite)
            sqlite_engine = create_engine(f"sqlite:///{sqlite_path}")
            SqliteSession = sessionmaker(bind=sqlite_engine)
            sqlite_session = SqliteSession()

            # Destination (Postgres)
            pg_engine = create_engine(settings.DATABASE_URL)
            PgSession = sessionmaker(bind=pg_engine)
            pg_session = PgSession()

            # Migrate Devices
            devices = sqlite_session.query(Device).all()
            for dev in devices:
                pg_session.merge(dev)
            pg_session.commit()

            # Migrate Readings in batches
            total = sqlite_session.query(Reading).count()
            batch_size = 500
            count = 0
            while count < total:
                chunk = sqlite_session.query(Reading).offset(count).limit(batch_size).all()
                for r in chunk:
                    pg_session.merge(r)
                pg_session.commit()
                count += len(chunk)
                print(f"✅ Migration Progress: {count}/{total}")

            print("🎉 Auto-migration completed successfully!")
            
            # Optionally rename the file so it doesn't run again
            os.rename(sqlite_path, f"{sqlite_path}.imported")

        except Exception as e:
            print(f"❌ Auto-migration failed: {e}")
        finally:
            sqlite_session.close()
            pg_session.close()

    migration_thread = threading.Thread(target=migrate, daemon=True)
    migration_thread.start()

def sync_postgres_sequences():
    """Resets PostgreSQL sequences to the current maximum ID to avoid collisions."""
    if not settings.DATABASE_URL.startswith("postgresql"):
        return

    from sqlalchemy import text
    try:
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            # Sync the 'readings' table sequence
            # Note: We use pg_get_serial_sequence to get the actual sequence name
            conn.execute(text("SELECT setval(pg_get_serial_sequence('readings', 'id'), (SELECT MAX(id) FROM readings))"))
            conn.commit()
            print("🔗 PostgreSQL sequences synchronized.")
    except Exception as e:
        print(f"⚠️ Could not sync sequences (may be empty or not Postgres): {e}")
