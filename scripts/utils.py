# scripts/utils.py

import logging
import os
import sqlite3

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

def get_database_connection(db_name):
    """
    Returns a connection to the specified SQLite database.
    """
    db_path = os.path.join(DATABASES_DIR, db_name)
    return sqlite3.connect(db_path)
