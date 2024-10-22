# ~/qfuse_backend/sensor_dashboard/app.py

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
    conn.execute('PRAGMA journal_mode=WAL;')  # Enable WAL mode
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
    Selects every 10th data point to reduce data volume.
    """
    device = request.args.get('device')
    subdevice = request.args.get('subdevice')
    since_id = request.args.get('since_id', type=int)

    query = "SELECT * FROM sensor_data"
    conditions = []
    params = []

    if device:
        conditions.append("device_id = ?")
        params.append(device)
    if subdevice:
        conditions.append("subdevice_id = ?")
        params.append(subdevice)
    if since_id is not None:
        conditions.append("id > ?")
        params.append(since_id)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # Select every 10th data point using modulo operator on 'id'
    query += " AND (id % 10 = 0)"
    query += " ORDER BY id ASC"  # Order data from oldest to newest

    conn = get_db_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()

    data = [dict(row) for row in rows]

    return jsonify(data)

if __name__ == '__main__':
    # Run the Flask app on all interfaces (0.0.0.0) and port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)