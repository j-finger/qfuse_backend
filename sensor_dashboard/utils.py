# utils.py
# scripts/utils.py
import logging
import os
import mariadb
import sys


# Determine the absolute path to the directory containing this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Determine the base directory (parent of scripts/)
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))

# Paths to the databases and logs directories
DATABASES_DIR = os.path.join(BASE_DIR, 'databases')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# Ensure the databases and logs directories exist
os.makedirs(DATABASES_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Configure logging
LOG_FILE = os.path.join(LOGS_DIR, 'backend.log')



logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# Database configuration
DATABASE_CONFIG = {
    'user': 'jaffers',       # Replace with your MariaDB username
    'password': '',   # Replace with your MariaDB password
    'host': 'localhost',
    'port': 3306,
    'database': 'sensor_data_db'   # Database name you created earlier
}

def get_database_connection():
    """
    Returns a connection to the MariaDB database.
    """
    try:
        conn = mariadb.connect(**DATABASE_CONFIG)
        return conn
    except mariadb.Error as e:
        logging.error(f"Error connecting to MariaDB: {e}")
        sys.exit(1)
