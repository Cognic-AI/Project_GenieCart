# app/database.py
import mysql.connector
from config.db_config import DB_CONFIG

def get_connection():
    """Establish and return a MySQL database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        raise Exception(f"Error connecting to MySQL: {err}")
