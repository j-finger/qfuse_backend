# app.py

from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Define the absolute path to the sensor_data.db
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, '..', 'databases', 'sensor_data.db')

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This allows us to fetch rows as dictionaries
    return conn

@app.route('/')
def index():
    """Renders the main dashboard page with filter options."""
    conn = get_db_connection()
    # Fetch distinct device_ids for the device filter dropdown
    devices = conn.execute('SELECT DISTINCT device_id FROM sensor_data').fetchall()
    # Fetch distinct subdevice_ids for the subdevice filter dropdown
    subdevices = conn.execute('SELECT DISTINCT subdevice_id FROM sensor_data').fetchall()
    conn.close()
    return render_template('index.html', devices=devices, subdevices=subdevices)

@app.route('/api/data')
def get_data():
    """
    API endpoint to fetch sensor data.
    Supports filtering by device_id and subdevice_id via query parameters.
    """
    device = request.args.get('device')
    subdevice = request.args.get('subdevice')

    query = "SELECT * FROM sensor_data"
    conditions = []
    params = []

    if device:
        conditions.append("device_id = ?")
        params.append(device)
    if subdevice:
        conditions.append("subdevice_id = ?")
        params.append(subdevice)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # Fetch the latest 1000 records; adjust as needed
    query += " ORDER BY id DESC LIMIT 1000"

    conn = get_db_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()

    # Convert rows to a list of dictionaries
    data = [dict(row) for row in rows]

    return jsonify(data)

if __name__ == '__main__':
    # Run the Flask app on all interfaces (0.0.0.0) and port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
