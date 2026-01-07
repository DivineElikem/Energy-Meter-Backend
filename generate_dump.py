import sqlite3
import os

def generate_pg_dump():
    sqlite_db = 'energy_meter.db'
    output_file = 'pg_dump.sql'
    
    if not os.path.exists(sqlite_db):
        print(f"❌ {sqlite_db} not found!")
        return

    conn = sqlite3.connect(sqlite_db)
    cursor = conn.cursor()

    with open(output_file, 'w') as f:
        # 1. Handle Devices
        print("📦 Processing devices...")
        cursor.execute("SELECT id, threshold FROM devices")
        devices = cursor.fetchall()
        for device_id, threshold in devices:
            # Use ON CONFLICT to avoid errors if some data is already there
            f.write(f"INSERT INTO devices (id, threshold) VALUES ('{device_id}', {threshold}) ON CONFLICT (id) DO UPDATE SET threshold = EXCLUDED.threshold;\n")

        # 2. Handle Readings
        print("📈 Processing readings (this might take a few moments)...")
        # We'll batch this to avoid memory issues
        cursor.execute("SELECT id, device, timestamp, current, voltage FROM readings")
        
        while True:
            rows = cursor.fetchmany(1000)
            if not rows:
                break
            for row in rows:
                rid, device, ts, curr, volt = row
                # Postgres timestamp format needs to be slightly cleaned if it's not and 's replaced
                f.write(f"INSERT INTO readings (id, device, timestamp, current, voltage) VALUES ({rid}, '{device}', '{ts}', {curr}, {volt}) ON CONFLICT (id) DO NOTHING;\n")

    conn.close()
    print(f"✅ Created {output_file}")
    print("\n🚀 TO IMPORT TO RENDER, RUN THIS COMMAND:")
    print("psql \"YOUR_EXTERNAL_DATABASE_URL\" -f pg_dump.sql")

if __name__ == "__main__":
    generate_pg_dump()
