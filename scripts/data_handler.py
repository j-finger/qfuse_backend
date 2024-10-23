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

        conn = get_database_connection()
        cursor = conn.cursor()

        for entry in data_list:
            logging.debug(f"Processing entry: {entry}")

            subdevice_id = entry.get('subdevice')
            timestamp = entry.get('timestamp')
            accel = entry.get('accel', {})
            gyro = entry.get('gyro', {})
            temperature = entry.get('temperature')

            # Convert data to appropriate types
            try:
                subdevice_id = int(subdevice_id) if subdevice_id is not None else None
            except ValueError:
                logging.error(f"Invalid subdevice_id value: {subdevice_id}")
                continue  # Skip this entry

            try:
                # Assuming timestamp is a hexadecimal string, convert to integer
                timestamp = int(timestamp, 16) if timestamp is not None else None
            except ValueError:
                logging.error(f"Invalid timestamp value: {timestamp}")
                continue  # Skip this entry

            try:
                temperature = float(temperature) if temperature is not None else None
            except ValueError:
                logging.error(f"Invalid temperature value: {temperature}")
                temperature = None  # Optional: set to None or skip entry

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
                logging.error(f"Invalid accel_x value: {accel_x}")
                accel_x = None  # Optional: set to None or skip entry

            try:
                accel_y = float(accel_y) if accel_y is not None else None
            except ValueError:
                logging.error(f"Invalid accel_y value: {accel_y}")
                accel_y = None  # Optional: set to None or skip entry

            try:
                accel_z = float(accel_z) if accel_z is not None else None
            except ValueError:
                logging.error(f"Invalid accel_z value: {accel_z}")
                accel_z = None  # Optional: set to None or skip entry

            try:
                gyro_x = float(gyro_x) if gyro_x is not None else None
            except ValueError:
                logging.error(f"Invalid gyro_x value: {gyro_x}")
                gyro_x = None  # Optional: set to None or skip entry

            try:
                gyro_y = float(gyro_y) if gyro_y is not None else None
            except ValueError:
                logging.error(f"Invalid gyro_y value: {gyro_y}")
                gyro_y = None  # Optional: set to None or skip entry

            try:
                gyro_z = float(gyro_z) if gyro_z is not None else None
            except ValueError:
                logging.error(f"Invalid gyro_z value: {gyro_z}")
                gyro_z = None  # Optional: set to None or skip entry

            # Log the values to be inserted
            logging.debug(
                f"Inserting data: device_id={device_id}, subdevice_id={subdevice_id}, "
                f"time={time}, timestamp={timestamp}, accel_x={accel_x}, "
                f"accel_y={accel_y}, accel_z={accel_z}, gyro_x={gyro_x}, "
                f"gyro_y={gyro_y}, gyro_z={gyro_z}, temperature={temperature}"
            )

            # Perform the database insertion
            try:
                cursor.execute(
                    '''
                    INSERT INTO sensor_data (
                        device_id, subdevice_id, time, timestamp,
                        accel_x, accel_y, accel_z,
                        gyro_x, gyro_y, gyro_z,
                        temperature
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ''',
                    (
                        device_id, subdevice_id, time, timestamp,
                        accel_x, accel_y, accel_z,
                        gyro_x, gyro_y, gyro_z,
                        temperature
                    )
                )
            except Exception as e:
                logging.error(f"Failed to insert data for subdevice {subdevice_id}: {e}")
                continue  # Skip to the next entry

        conn.commit()
        cursor.close()
        conn.close()
        logging.info(f"Processed {len(data_list)} data entries for device {device_id}.")
    except Exception as e:
        logging.error(f"Error in handle_data_message: {e}")
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

        conn = get_database_connection()
        cursor = conn.cursor()

        for entry in data_list:
            logging.debug(f"Processing entry: {entry}")

            subdevice_id = entry.get('subdevice')
            timestamp = entry.get('timestamp')
            accel = entry.get('accel', {})
            gyro = entry.get('gyro', {})
            temperature = entry.get('temperature')

            # Convert data to appropriate types
            try:
                subdevice_id = int(subdevice_id) if subdevice_id is not None else None
            except ValueError:
                logging.error(f"Invalid subdevice_id value: {subdevice_id}")
                continue  # Skip this entry

            try:
                # Assuming timestamp is a hexadecimal string, convert to integer
                timestamp = int(timestamp, 16) if timestamp is not None else None
            except ValueError:
                logging.error(f"Invalid timestamp value: {timestamp}")
                continue  # Skip this entry

            try:
                temperature = float(temperature) if temperature is not None else None
            except ValueError:
                logging.error(f"Invalid temperature value: {temperature}")
                temperature = None  # Optional: set to None or skip entry

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
                logging.error(f"Invalid accel_x value: {accel_x}")
                accel_x = None  # Optional: set to None or skip entry

            try:
                accel_y = float(accel_y) if accel_y is not None else None
            except ValueError:
                logging.error(f"Invalid accel_y value: {accel_y}")
                accel_y = None  # Optional: set to None or skip entry

            try:
                accel_z = float(accel_z) if accel_z is not None else None
            except ValueError:
                logging.error(f"Invalid accel_z value: {accel_z}")
                accel_z = None  # Optional: set to None or skip entry

            try:
                gyro_x = float(gyro_x) if gyro_x is not None else None
            except ValueError:
                logging.error(f"Invalid gyro_x value: {gyro_x}")
                gyro_x = None  # Optional: set to None or skip entry

            try:
                gyro_y = float(gyro_y) if gyro_y is not None else None
            except ValueError:
                logging.error(f"Invalid gyro_y value: {gyro_y}")
                gyro_y = None  # Optional: set to None or skip entry

            try:
                gyro_z = float(gyro_z) if gyro_z is not None else None
            except ValueError:
                logging.error(f"Invalid gyro_z value: {gyro_z}")
                gyro_z = None  # Optional: set to None or skip entry

            # Log the values to be inserted
            logging.debug(
                f"Inserting data: device_id={device_id}, subdevice_id={subdevice_id}, "
                f"time={time}, timestamp={timestamp}, accel_x={accel_x}, "
                f"accel_y={accel_y}, accel_z={accel_z}, gyro_x={gyro_x}, "
                f"gyro_y={gyro_y}, gyro_z={gyro_z}, temperature={temperature}"
            )

            # Perform the database insertion
            try:
                cursor.execute(
                    '''
                    INSERT INTO sensor_data (
                        device_id, subdevice_id, time, timestamp,
                        accel_x, accel_y, accel_z,
                        gyro_x, gyro_y, gyro_z,
                        temperature
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ''',
                    (
                        device_id, subdevice_id, time, timestamp,
                        accel_x, accel_y, accel_z,
                        gyro_x, gyro_y, gyro_z,
                        temperature
                    )
                )
            except Exception as e:
                logging.error(f"Failed to insert data for subdevice {subdevice_id}: {e}")
                continue  # Skip to the next entry

        conn.commit()
        cursor.close()
        conn.close()
        logging.info(f"Processed {len(data_list)} data entries for device {device_id}.")
    except Exception as e:
        logging.error(f"Error in handle_data_message: {e}")
