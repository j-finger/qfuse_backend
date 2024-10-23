# app.py
# ~/qfuse_backend/sensor_dashboard/app.py

from flask import Flask, render_template, request, jsonify
import mariadb
import sys
import os
from utils import get_database_connection

app = Flask(__name__)

@app.route('/')
def index():
    """Renders the main dashboard page with filter options."""
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)
    # Fetch distinct device_ids for the device filter dropdown
    cursor.execute('SELECT DISTINCT device_id FROM sensor_data')
    devices = cursor.fetchall()
    # Fetch distinct subdevice_ids for the subdevice filter dropdown
    cursor.execute('SELECT DISTINCT subdevice_id FROM sensor_data')
    subdevices = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', devices=devices, subdevices=subdevices)

# @app.route('/api/data')
# def get_data():
#     """
#     API endpoint to fetch sensor data.
#     Supports filtering by device_id and subdevice_id via query parameters.
#     Selects every 10th data point to reduce data volume.
#     """
#     device = request.args.get('device')
#     subdevice = request.args.get('subdevice')
#     since_id = request.args.get('since_id', type=int)

#     query = "SELECT * FROM sensor_data"
#     conditions = []
#     params = []

#     if device:
#         conditions.append("device_id = %s")
#         params.append(device)
#     if subdevice:
#         conditions.append("subdevice_id = %s")
#         params.append(subdevice)
#     if since_id is not None:
#         conditions.append("id > %s")
#         params.append(since_id)

#     # Add the modulo condition to select every 10th data point
#     # conditions.append("(id % 10 = 0)")

#     if conditions:
#         query += " WHERE " + " AND ".join(conditions)

#     query += " ORDER BY id ASC"  # Order data from oldest to newest

#     conn = get_database_connection()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute(query, params)
#     rows = cursor.fetchall()
#     cursor.close()
#     conn.close()

    # return jsonify(rows)

@app.route('/api/data')
def get_data():
    device = request.args.get('device')
    subdevice = request.args.get('subdevice', type=int)
    since_id = request.args.get('since_id', type=int)

    # Base query with window function
    base_query = '''
    SELECT * FROM (
        SELECT 
            *,
            ROW_NUMBER() OVER (PARTITION BY subdevice_id ORDER BY id ASC) as rn
        FROM sensor_data
        {where_clause}
    ) t
    WHERE t.rn % 10 = 0
    ORDER BY t.id ASC
    '''

    conditions = []
    params = []

    if device:
        conditions.append("device_id = %s")
        params.append(device)
    if subdevice is not None:
        conditions.append("subdevice_id = %s")
        params.append(subdevice)
    if since_id is not None:
        conditions.append("id > %s")
        params.append(since_id)

    where_clause = ''
    if conditions:
        where_clause = 'WHERE ' + ' AND '.join(conditions)

    query = base_query.format(where_clause=where_clause)

    # Debugging output
    print(f"Executing query: {query}")
    print(f"With parameters: {params}")

    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(rows)



if __name__ == '__main__':
    # Run the Flask app on all interfaces (0.0.0.0) and port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
