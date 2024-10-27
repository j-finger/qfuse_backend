
## Raspberry Pi Backend and Frontend for `qfuse` Data Acquisition System

### Overview

This repository contains the backend and frontend code for the `qfuse` data acquisition system, designed to run on a Raspberry Pi 4. The Raspberry Pi acts as a central server, hosting an MQTT broker for data ingestion, a Flask web application for data visualization, and handles data storage in a MariaDB database. The backend processes sensor data received from the ESP32C6 modules and stores it for further analysis, while the frontend provides a dashboard for real-time data visualization and monitoring.

### Features

- **MQTT Broker**: Hosts an MQTT broker to receive sensor data from multiple `qfuse` devices.
- **Data Storage**: Stores sensor data, settings, and logs in a MariaDB database.
- **Data Processing**: Parses and processes incoming JSON data, handling different message types.
- **Flask Web Application**: Provides a web-based dashboard for data visualization with real-time charts.
- **RESTful API**: Offers an API endpoint to fetch sensor data for the frontend.
- **Network Configuration Management**: Includes a network switcher script to toggle between AP and Client modes.
- **Logging and Error Handling**: Implements detailed logging for troubleshooting and system monitoring.

### Hardware Setup

#### Components

- **Raspberry Pi 4**: Acts as the backend server and frontend host.
- **ESP32C6 Modules**: Send sensor data to the Raspberry Pi via MQTT over Wi-Fi.
- **`qfuse` Development Boards**: Collect sensor data and transmit it through the ESP32C6 modules.

#### Network Configuration

- **Access Point Mode**: The Raspberry Pi can act as a Wi-Fi access point (`qfnet`) for direct connections from ESP32C6 modules.
- **Client Mode**: The Raspberry Pi connects to a preconfigured Wi-Fi network (`preconfigured`).

#### GPIO Pins

- **Switch Pin**: GPIO 21 (Connected to a toggle switch for network mode switching).
- **LED Indicators**:
	- **LED_WIFI_PIN**: GPIO 7 (Indicates Wi-Fi connection status).
	- **LED_LAN_PIN**: GPIO 10 (Indicates LAN connection status).

### Software Dependencies

- **Operating System**: Raspberry Pi OS (32-bit or 64-bit).
- **Python 3.x**: For running scripts and Flask application.
- **MariaDB**: For data storage.
- **Flask**: Web framework for the frontend application.
- **Paho-MQTT**: MQTT client library for Python.
- **Chart.js**: JavaScript library for data visualization in the frontend.
- **RPi.GPIO**: For GPIO pin control in Python.
- **Subprocess**: For executing shell commands from Python scripts.
- **Systemd**: For managing services like `mqtt_listener.service`.

### Directory Structure

- `app.py`: Main Flask application file for the frontend.
- `scripts/`: Contains backend scripts and utilities.
	- `mqtt_listener.py`: Listens to MQTT topics and processes incoming messages.
	- `data_handler.py`: Handles incoming sensor data and stores it in the database.
	- `settings_handler.py`: Processes settings messages.
	- `logs_handler.py`: Processes log messages.
	- `initialize_databases.py`: Initializes the database tables.
	- `network_switcher.py`: Manages network mode switching via GPIO.
	- `viewer.py`: Utility script to view database entries.
	- `utils.py`: Contains common utility functions and configurations.
- `templates/`: Contains HTML templates for the Flask application.
	- `index.html`: Main dashboard page.
- `static/`: Contains static files for the frontend.
	- `js/charts.js`: JavaScript file for rendering charts using Chart.js.
- `logs/`: Directory for log files.
	- `backend.log`: Log file for backend operations.
- `databases/`: Directory for database files (if using SQLite, but MariaDB is used here).

### Setup Instructions

#### Prerequisites

1. **Update System Packages**:

   ```bash
   sudo apt update
   sudo apt upgrade
   ```

2. **Install Python 3 and Pip**:

   ```bash
   sudo apt install python3 python3-pip
   ```

3. **Install MariaDB**:

   ```bash
   sudo apt install mariadb-server
   ```

4. **Install Required Python Packages**:

   ```bash
   pip3 install flask mariadb paho-mqtt RPi.GPIO
   ```

#### Database Configuration

1. **Secure MariaDB Installation**:

   ```bash
   sudo mysql_secure_installation
   ```

   - Set a root password.
   - Remove anonymous users.
   - Disallow root login remotely.
   - Remove test database.
   - Reload privilege tables.

2. **Create Database and User**:

   ```bash
   sudo mariadb
   ```

   In the MariaDB shell:

   ```sql
   CREATE DATABASE sensor_data_db;
   CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';
   GRANT ALL PRIVILEGES ON sensor_data_db.* TO 'username'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```

   Replace `'username'` and `'password'` with your desired credentials.

3. **Initialize Database Tables**:

   ```bash
   python3 scripts/initialize_databases.py
   ```

#### MQTT Broker Setup

1. **Install Mosquitto MQTT Broker**:
   ```bash
   sudo apt install mosquitto mosquitto-clients
   ```
2. **Configure Mosquitto (Optional)**:
   - Edit `/etc/mosquitto/mosquitto.conf` to adjust configurations if necessary.
   - Restart Mosquitto service:
     ```bash
     sudo systemctl restart mosquitto
     ```

#### Flask Application Setup

1. **Set Environment Variables**:
   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development  # Remove or change to 'production' in production environment
   ```
2. **Run the Flask Application**:
   ```bash
   flask run --host=0.0.0.0 --port=5000
   ```
   - The application will be accessible at `http://<raspberry_pi_ip>:5000`.

#### Backend Services Setup

1. **Set Up MQTT Listener as a Service**:

   - Create a systemd service file `/etc/systemd/system/mqtt_listener.service`:
```ini
[Unit]
Description=MQTT Listener Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/scripts/mqtt_listener.py
WorkingDirectory=/path/to/scripts
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```
 Replace `/path/to/scripts` with the actual path to your `scripts/` directory.
   - Reload systemd and start the service:
     ```bash
     sudo systemctl daemon-reload
     sudo systemctl enable mqtt_listener.service
     sudo systemctl start mqtt_listener.service
     ```
2. **Set Up Network Switcher Script**:
   - Ensure the `network_switcher.py` script is running at startup.
   - Add it to `rc.local` or create a systemd service for it.

#### GPIO Permissions

- Add your user to the `gpio` group:
  ```bash
  sudo adduser pi gpio
  ```
- Install `python3-rpi.gpio`:
  ```bash
  sudo apt install python3-rpi.gpio
  ```

### Usage Instructions

#### Running the Backend

- The `mqtt_listener.py` script runs as a service and listens for incoming MQTT messages on the topics:
	- `sensor/data`
	- `sensor/settings`
	- `sensor/logs`
	- `time/request`
- Incoming messages are processed and stored in the MariaDB database.

#### Accessing the Frontend Dashboard

- Navigate to `http://<raspberry_pi_ip>:5000` in a web browser.
- Use the filter options to select specific devices or subdevices.
- The dashboard displays real-time charts for accelerometer and gyroscope data.

#### Switching Network Modes

- Use the physical toggle switch connected to GPIO 21 to switch between AP Mode and Client Mode.
- **AP Mode**:
	- Raspberry Pi acts as a Wi-Fi access point (`qfnet`).
	- ESP32C6 modules connect directly to the Raspberry Pi.
- **Client Mode**:
	- Raspberry Pi connects to a preconfigured Wi-Fi network (`preconfigured`).
	- Ensure that the network credentials are correctly set in the Raspberry Pi's network manager.
- LED Indicators:
	- **LED_WIFI_PIN (GPIO 7)**: Indicates Wi-Fi connection status.
	- **LED_LAN_PIN (GPIO 10)**: Indicates LAN connection status.

### Code Organization

#### `app.py`

- **Flask Application**:
	- Renders the main dashboard page with filter options.
	- Provides an API endpoint `/api/data` to fetch sensor data in JSON format.
	- Supports filtering by `device_id` and `subdevice_id`.

#### `scripts/`

- **`mqtt_listener.py`**:
	- Connects to the MQTT broker and subscribes to relevant topics.
	- Dispatches incoming messages to appropriate handlers.
- **`data_handler.py`**:
	- Processes incoming sensor data messages.
	- Parses JSON payloads and inserts data into the `sensor_data` table.
- **`settings_handler.py`**:
	- Handles settings messages and stores them in the `settings` table.
- **`logs_handler.py`**:
	- Processes log messages and stores them in the `logs` table.
- **`network_switcher.py`**:
	- Monitors the toggle switch state and switches network modes accordingly.
	- Controls LED indicators to reflect the current network status.
- **`initialize_databases.py`**:
	- Initializes the required database tables if they do not exist.
- **`utils.py`**:
	- Contains utility functions such as database connection management and logging configuration.

#### `templates/index.html`

- **HTML Template**:
	- Defines the structure of the dashboard page.
	- Includes placeholders for device and subdevice filter options.
	- References JavaScript files for chart rendering.

#### `static/js/charts.js`

- **JavaScript for Data Visualization**:
	- Uses Chart.js to render real-time charts for accelerometer and gyroscope data.
	- Fetches data from the `/api/data` endpoint.
	- Implements incremental data fetching and chart updating.

### Configuration

#### Database Configuration

- **MariaDB Credentials**:
	- Set in `utils.py` under `DATABASE_CONFIG`.
	- Ensure that the user and password match what was set during database setup.

#### MQTT Broker Configuration

- **MQTT Topics**:
	- Defined in `mqtt_listener.py` under `MQTT_TOPICS`.
	- Ensure that the ESP32C6 modules publish to these topics.
- **Broker Address**:
	- By default, the broker is hosted locally (`localhost`).
	- If the broker is hosted elsewhere, update the `MQTT_BROKER` variable.

#### Network Configuration

- **Network Manager Connection Names**:
	- Defined in `network_switcher.py` as `AP_MODE` and `CLIENT_MODE`.
	- Ensure that these names match the connection profiles in Network Manager.
- **GPIO Pins**:
	- Switch and LED pins are defined in `network_switcher.py`.
	- Adjust if different GPIO pins are used.

#### Flask Application

- **Host and Port**:
	- By default, the Flask app runs on `0.0.0.0` and port `5000`.
	- Adjust in `app.py` or when running the `flask run` command.

### Troubleshooting

- **Cannot Connect to the MQTT Broker**:
	- Ensure that Mosquitto is running:
    ```bash
    sudo systemctl status mosquitto
    ```
	- Check firewall settings to ensure the broker port (`1883`) is open.
- **Database Connection Errors**:
	- Verify MariaDB is running:
    ```bash
    sudo systemctl status mariadb
    ```
	- Ensure that the database credentials in `utils.py` are correct.
- **Flask Application Not Accessible**:
	- Confirm the Flask app is running without errors.
	- Check that the correct IP address and port are used.
	- Ensure no firewall rules are blocking port `5000`.
- **Network Switching Not Working**:
	- Check GPIO connections and ensure the toggle switch is functioning.
	- Verify that the `network_switcher.py` script is running.
	- Review logs in `backend.log` for any error messages.
- **Data Not Displaying on Dashboard**:
	- Confirm that data is being received and stored in the database.
	- Use `viewer.py` to inspect database entries.
	- Check browser console for any JavaScript errors.

### Future Work

- **Implement Authentication**:
	- Add user authentication to the Flask application for secure access.
- **Data Aggregation and Analysis**:
	- Implement data aggregation functions for long-term data analysis.
	- Develop algorithms for sensor fusion and anomaly detection.
- **Enhanced Visualization**:
	- Add more charts and graphs to display additional data metrics.
	- Implement real-time updates using WebSockets.
- **Scalability Improvements**:
	- Optimize database queries and indexing for better performance.
	- Implement data retention policies and archival strategies.
- **Security Enhancements**:
	- Secure MQTT communication using TLS.
	- Implement input validation and sanitization throughout the application.

### License

This project is licensed under the [MIT License](LICENSE).

### Acknowledgments

- **Flask**: For the web framework used in the frontend.
- **MariaDB**: For the database management system.
- **Mosquitto**: For the MQTT broker.
- **Chart.js**: For providing the charting library.
- **Raspberry Pi Community**: For extensive documentation and support.
- **Open Source Contributors**: For various libraries and tools utilized.

