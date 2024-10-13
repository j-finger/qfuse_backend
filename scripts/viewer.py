# scripts/viewer.py

import sqlite3
import logging
from utils import get_database_connection

def view_table(db_name, table_name, limit=10):
    try:
        conn = get_database_connection(db_name)
        c = conn.cursor()
        c.execute(f'SELECT * FROM {table_name} LIMIT ?', (limit,))
        rows = c.fetchall()
        conn.close()
        return rows
    except Exception as e:
        logging.error(f"Error viewing table {table_name} in {db_name}: {e}")
        return []

def main():
    logging.info("Viewing sample data from databases...\n")

    print("Sensor Data:")
    sensor_data = view_table('sensor_data.db', 'sensor_data')
    for row in sensor_data:
        print(row)

    print("\nSettings:")
    settings = view_table('settings.db', 'settings')
    for row in settings:
        print(row)

    print("\nLogs:")
    logs = view_table('logs.db', 'logs')
    for row in logs:
        print(row)

if __name__ == '__main__':
    main()
