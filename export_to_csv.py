import sqlite3
import pandas as pd
import os

def export_to_csv():
    db_path = 'energy_meter.db'
    if not os.path.exists(db_path):
        print("❌ SQLite file not found!")
        return

    conn = sqlite3.connect(db_path)
    
    # Export Devices
    print("📦 Exporting devices...")
    devices = pd.read_sql_query("SELECT * FROM devices", conn)
    devices.to_csv('devices_backup.csv', index=False)
    
    # Export Readings
    print("📈 Exporting readings (this might take a second)...")
    readings = pd.read_sql_query("SELECT * FROM readings", conn)
    readings.to_csv('readings_backup.csv', index=False)
    
    conn.close()
    print("✅ Done! Created 'devices_backup.csv' and 'readings_backup.csv'")

if __name__ == "__main__":
    export_to_csv()
