# viewer.py
# scripts/viewer.py

import logging
from utils import get_database_connection

def view_table(table_name, limit=10):
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {table_name} LIMIT %s', (limit,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        logging.error(f"Error viewing table {table_name}: {e}")
        return []

def main():
    logging.info("Viewing sample data from the database...\n")

    print("Sensor Data:")
    sensor_data = view_table('sensor_data')
    for row in sensor_data:
        print(row)

    print("\nSettings:")
    settings = view_table('settings')
    for row in settings:
        print(row)

    print("\nLogs:")
    logs = view_table('logs')
    for row in logs:
        print(row)

if __name__ == '__main__':
    main()
