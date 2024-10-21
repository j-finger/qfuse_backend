# data_handler.py
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

            # Convert data to appropriate types
            try:
                subdevice_id = int(subdevice_id) if subdevice_id is not None else None
            except ValueError:
                subdevice_id = None
                logging.error("Invalid subdevice_id value.")

            try:
                # Assuming timestamp is a hexadecimal string, convert to integer
                timestamp = int(timestamp, 16) if timestamp is not None else None
            except ValueError:
                timestamp = None
                logging.error("Invalid timestamp value.")

            try:
                temperature = float(temperature) if temperature is not None else None
            except ValueError:
                temperature = None
                logging.error("Invalid temperature value.")

            accel_x = accel.get('x')
            accel_y = accel.get('y')
            accel_z = accel.get('z')
            gyro_x = gyro.get('x')
            gyro_y = gyro.get('y')
            gyro_z = gyro.get('z')

            # Convert accel and gyro values to float
            try:
                accel_x = float(accel_x) if accel_x is not None else None
            except ValueError:
                accel_x = None
                logging.error("Invalid accel_x value.")

            try:
                accel_y = float(accel_y) if accel_y is not None else None
            except ValueError:
                accel_y = None
                logging.error("Invalid accel_y value.")

            try:
                accel_z = float(accel_z) if accel_z is not None else None
            except ValueError:
                accel_z = None
                logging.error("Invalid accel_z value.")

            try:
                gyro_x = float(gyro_x) if gyro_x is not None else None
            except ValueError:
                gyro_x = None
                logging.error("Invalid gyro_x value.")

            try:
                gyro_y = float(gyro_y) if gyro_y is not None else None
            except ValueError:
                gyro_y = None
                logging.error("Invalid gyro_y value.")

            try:
                gyro_z = float(gyro_z) if gyro_z is not None else None
            except ValueError:
                gyro_z = None
                logging.error("Invalid gyro_z value.")

            # Perform the database insertion
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
