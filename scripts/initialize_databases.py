# scripts/initialize_databases.py

import sqlite3
import os
import logging
from utils import get_database_connection, DATABASES_DIR

def create_databases():
    logging.info("Initializing databases...")

    # Sensor Data Database
    conn = get_database_connection('sensor_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT,
            subdevice_id INTEGER,
            time TEXT,
            timestamp TEXT,
            accel_x REAL,
            accel_y REAL,
            accel_z REAL,
            gyro_x REAL,
            gyro_y REAL,
            gyro_z REAL,
            temperature REAL
        )
    ''')
    conn.commit()
    conn.close()
    logging.info("Initialized sensor_data.db")

    # Settings Database
    conn = get_database_connection('settings.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT,
            time TEXT,
            subdevice_id INTEGER,
            accel_odr TEXT,
            accel_fsr TEXT,
            accel_sensitivity REAL,
            gyro_odr TEXT,
            gyro_fsr TEXT,
            gyro_sensitivity REAL,
            accel_mode TEXT,
            gyro_mode TEXT
        )
    ''')
    conn.commit()
    conn.close()
    logging.info("Initialized settings.db")

    # Logs Database
    conn = get_database_connection('logs.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT,
            time TEXT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()
    logging.info("Initialized logs.db")

if __name__ == '__main__':
    create_databases()
    logging.info("All databases have been initialized successfully.")
