# initialize_databases.py
# scripts/initialize_databases.py

import logging
from utils import get_database_connection

def create_tables():
    logging.info("Initializing tables...")

    conn = get_database_connection()
    cursor = conn.cursor()

    # Sensor Data Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            device_id VARCHAR(255),
            subdevice_id INT,
            time VARCHAR(255),
            timestamp VARCHAR(255),
            accel_x FLOAT,
            accel_y FLOAT,
            accel_z FLOAT,
            gyro_x FLOAT,
            gyro_y FLOAT,
            gyro_z FLOAT,
            temperature FLOAT
        )
    ''')
    logging.info("Created sensor_data table.")

    # Settings Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            device_id VARCHAR(255),
            time VARCHAR(255),
            subdevice_id INT,
            accel_odr VARCHAR(255),
            accel_fsr VARCHAR(255),
            accel_sensitivity FLOAT,
            gyro_odr VARCHAR(255),
            gyro_fsr VARCHAR(255),
            gyro_sensitivity FLOAT,
            accel_mode VARCHAR(255),
            gyro_mode VARCHAR(255)
        )
    ''')
    logging.info("Created settings table.")

    # Logs Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            device_id VARCHAR(255),
            time VARCHAR(255),
            message TEXT
        )
    ''')
    logging.info("Created logs table.")

    conn.commit()
    cursor.close()
    conn.close()
    logging.info("All tables have been initialized successfully.")

if __name__ == '__main__':
    create_tables()
