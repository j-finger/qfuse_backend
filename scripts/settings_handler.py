# scripts/settings_handler.py

import logging
from utils import get_database_connection

def handle_settings_message(data):
    try:
        device_id = data.get('device')
        time = data.get('time')
        settings = data.get('settings', {})

        if not settings:
            logging.warning("No settings found in the message.")
            return

        subdevice_id = settings.get('subdevice')
        accel_odr = settings.get('accel_odr')
        accel_fsr = settings.get('accel_fsr')
        accel_sensitivity = settings.get('accel_sensitivity')
        gyro_odr = settings.get('gyro_odr')
        gyro_fsr = settings.get('gyro_fsr')
        gyro_sensitivity = settings.get('gyro_sensitivity')
        power = settings.get('power', {})
        accel_mode = power.get('accel_mode')
        gyro_mode = power.get('gyro_mode')

        conn = get_database_connection('settings.db')
        c = conn.cursor()

        c.execute('''
            INSERT INTO settings (
                device_id, time, subdevice_id,
                accel_odr, accel_fsr, accel_sensitivity,
                gyro_odr, gyro_fsr, gyro_sensitivity,
                accel_mode, gyro_mode
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            device_id, time, subdevice_id,
            accel_odr, accel_fsr, accel_sensitivity,
            gyro_odr, gyro_fsr, gyro_sensitivity,
            accel_mode, gyro_mode
        ))

        conn.commit()
        conn.close()
        logging.info(f"Settings updated for device {device_id}, subdevice {subdevice_id}.")
    except Exception as e:
        logging.error(f"Error in handle_settings_message: {e}")
