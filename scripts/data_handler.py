# scripts/data_handler.py

import logging
from utils import get_database_connection

def handle_data_message(data):
    try:
        device_id = data.get('device')
        time = data.get('time')
        data_list = data.get('data', [])

        if not data_list:
            logging.warning("No data entries found in the message.")
            return

        conn = get_database_connection('sensor_data.db')
        c = conn.cursor()

        for entry in data_list:
            subdevice_id = entry.get('subdevice')
            timestamp = entry.get('timestamp')
            accel = entry.get('accel', {})
            gyro = entry.get('gyro', {})
            temperature = entry.get('temperature')

            accel_x = accel.get('x')
            accel_y = accel.get('y')
            accel_z = accel.get('z')

            gyro_x = gyro.get('x')
            gyro_y = gyro.get('y')
            gyro_z = gyro.get('z')

            c.execute('''
                INSERT INTO sensor_data (
                    device_id, subdevice_id, time, timestamp,
                    accel_x, accel_y, accel_z,
                    gyro_x, gyro_y, gyro_z,
                    temperature
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                device_id, subdevice_id, time, timestamp,
                accel_x, accel_y, accel_z,
                gyro_x, gyro_y, gyro_z,
                temperature
            ))

        conn.commit()
        conn.close()
        logging.info(f"Inserted {len(data_list)} data entries for device {device_id}.")
    except Exception as e:
        logging.error(f"Error in handle_data_message: {e}")
