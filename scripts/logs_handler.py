# scripts/logs_handler.py

import logging
from utils import get_database_connection

def handle_logs_message(data):
    try:
        device_id = data.get('device')
        time = data.get('time')
        message = data.get('log')

        if not message:
            logging.warning("No log message found.")
            return

        conn = get_database_connection('logs.db')
        c = conn.cursor()

        c.execute('''
            INSERT INTO logs (device_id, time, message)
            VALUES (?, ?, ?)
        ''', (device_id, time, message))

        conn.commit()
        conn.close()
        logging.info(f"Log entry added for device {device_id}.")
    except Exception as e:
        logging.error(f"Error in handle_logs_message: {e}")
