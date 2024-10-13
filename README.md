# qfuse Backend Scripts

## Overview

The `qfuse` backend consists of a suite of Python scripts designed to handle data transmission, processing, and storage for the `qfuse` project. This backend facilitates the reception of sensor data, settings, and logs via MQTT, processes the received JSON packets, and stores the information in SQLite3 databases. Additionally, it provides utilities for initializing databases and viewing stored data.

## Features

- **MQTT Integration**: Receives data through MQTT topics (`sensor/data`, `sensor/settings`, `sensor/logs`).
- **Data Processing**: Parses JSON packets and inserts data into appropriate SQLite3 databases.
- **Database Management**: Initializes and manages SQLite3 databases for sensor data, settings, and logs.
- **Logging**: Comprehensive logging for monitoring and debugging.
- **Data Visualization**: Simple script to view stored data from databases.

## Prerequisites

- **Python**: Version 3.7 or higher.
- **MQTT Broker**: Mosquitto MQTT Server or any compatible broker.
- **SQLite3**: For database management.
- **Python Packages**:
  - `paho-mqtt`
  - `sqlite3` (usually included with Python)
  - `logging`

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/qfuse-backend.git
   cd qfuse-backend/scripts
   ```

2. **Set Up a Virtual Environment (Optional but Recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Required Python Packages**

   ```bash
   pip install paho-mqtt
   ```

   *Note: If you have a `requirements.txt` file, you can install all dependencies at once:*

   ```bash
   pip install -r requirements.txt
   ```

## Setup

### Initialize Databases

Before running the backend scripts, initialize the necessary SQLite3 databases.

```bash
python initialize_databases.py
```

This script will create the following databases in the `databases/` directory:

- `sensor_data.db`: Stores sensor data from IMU sensors.
- `settings.db`: Stores device settings.
- `logs.db`: Stores log messages.

## Usage

### Running the MQTT Listener

Start the MQTT listener to begin receiving and processing data from the `qfuse` devices.

```bash
python mqtt_listener.py
```

**What It Does:**

- Connects to the MQTT broker at `localhost` on port `1883`.
- Subscribes to the following MQTT topics:
  - `sensor/data`
  - `sensor/settings`
  - `sensor/logs`
- Processes incoming messages and delegates them to appropriate handlers:
  - `sensor/data` → `data_handler.py`
  - `sensor/settings` → `settings_handler.py`
  - `sensor/logs` → `logs_handler.py`

**Note:** Ensure that the MQTT broker is running and accessible at the specified address and port.

### Viewing Data

To view sample data from the databases, use the `viewer.py` script.

```bash
python viewer.py
```

**What It Does:**

- Connects to each SQLite3 database (`sensor_data.db`, `settings.db`, `logs.db`).
- Retrieves and prints the first 10 entries from each table:
  - `sensor_data`
  - `settings`
  - `logs`

**Example Output:**

```
Viewing sample data from databases...

Sensor Data:
(1, 'E46338809B472231', 1, '1728792656', '0000C8', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 25.0)
(2, 'E46338809B472231', 1, '1728792656', '0000C9', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 25.1)

Settings:
(1, 'E46338809B472231', '1728792656', 1, '100Hz', '±4g', 8192.0, '100Hz', '±500dps', 65.5, 'Low Noise', 'Low Noise')

Logs:
(1, 'E46338809B472231', '1728792656', 'some log line')
```

## Project Structure

```
qfuse-backend/
├── databases/
│   ├── sensor_data.db
│   ├── settings.db
│   └── logs.db
├── logs/
│   └── backend.log
├── scripts/
│   ├── data_handler.py
│   ├── initialize_databases.py
│   ├── logs_handler.py
│   ├── mqtt_listener.py
│   ├── settings_handler.py
│   ├── utils.py
│   └── viewer.py
├── requirements.txt
└── README.md
```

- **databases/**: Contains SQLite3 database files.
- **logs/**: Contains the backend log file (`backend.log`).
- **scripts/**: Contains all backend Python scripts.
- **requirements.txt**: Lists Python dependencies (if available).
- **README.md**: Project documentation (this file).

## Scripts Description

### data_handler.py

**Location:** `scripts/data_handler.py`

**Description:**

Handles incoming sensor data messages from the `sensor/data` MQTT topic. It parses the JSON payload and inserts the sensor readings into the `sensor_data.db` database.

**Key Functions:**

- `handle_data_message(data)`: Processes the sensor data and performs database insertion.

### initialize_databases.py

**Location:** `scripts/initialize_databases.py`

**Description:**

Initializes the SQLite3 databases by creating the necessary tables if they do not already exist.

**Key Functions:**

- `create_databases()`: Creates `sensor_data.db`, `settings.db`, and `logs.db` with their respective tables.

**Usage:**

```bash
python initialize_databases.py
```

### logs_handler.py

**Location:** `scripts/logs_handler.py`

**Description:**

Handles incoming log messages from the `sensor/logs` MQTT topic. It parses the JSON payload and inserts log messages into the `logs.db` database.

**Key Functions:**

- `handle_logs_message(data)`: Processes the log message and performs database insertion.

### mqtt_listener.py

**Location:** `scripts/mqtt_listener.py`

**Description:**

Listens to MQTT topics (`sensor/data`, `sensor/settings`, `sensor/logs`) and delegates message handling to the appropriate handlers. Manages MQTT connection and subscription.

**Key Functions:**

- `on_connect(client, userdata, flags, rc)`: Callback for MQTT connection.
- `on_message(client, userdata, msg)`: Callback for incoming MQTT messages.
- `main()`: Initializes and starts the MQTT client loop.

**Usage:**

```bash
python mqtt_listener.py
```

### settings_handler.py

**Location:** `scripts/settings_handler.py`

**Description:**

Handles incoming settings messages from the `sensor/settings` MQTT topic. It parses the JSON payload and updates the device settings in the `settings.db` database.

**Key Functions:**

- `handle_settings_message(data)`: Processes the settings data and performs database insertion.

### utils.py

**Location:** `scripts/utils.py`

**Description:**

Provides utility functions and configurations used by other scripts, including database connection management and logging setup.

**Key Components:**

- **Directories:**
  - `DATABASES_DIR`: Path to the `databases/` directory.
  - `LOGS_DIR`: Path to the `logs/` directory.
- **Logging Configuration:**
  - Logs are written to `logs/backend.log` and also output to the console.
- **Functions:**
  - `get_database_connection(db_name)`: Returns a connection to the specified SQLite database.

**Note:** This script ensures that the `databases/` and `logs/` directories exist, creating them if necessary.

### viewer.py

**Location:** `scripts/viewer.py`

**Description:**

A utility script to view sample data from the databases. It prints the first 10 entries from each table (`sensor_data`, `settings`, `logs`) to the console.

**Key Functions:**

- `view_table(db_name, table_name, limit=10)`: Retrieves and returns rows from a specified table.
- `main()`: Executes the viewing of sample data.

**Usage:**

```bash
python viewer.py
```

## Logging

All backend activities are logged in the `logs/backend.log` file. Logs include:

- **INFO**: Successful operations (e.g., database insertions, MQTT connections).
- **WARNING**: Potential issues (e.g., missing data in messages).
- **ERROR**: Failures or exceptions during processing.

**Example Log Entry:**

```
2024-04-27 10:15:30,123 INFO:Inserted 2 data entries for device E46338809B472231.
2024-04-27 10:15:31,456 ERROR:Error in handle_data_message: SQLite3 error message
```

**Log Configuration:**

- Logs are written to both the log file (`logs/backend.log`) and the console.
- Logging level is set to `INFO` by default.

## License

This project is licensed under the [MIT License](LICENSE).
