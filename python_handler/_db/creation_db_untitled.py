import sqlite3
import os
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("db_creation.log"),
        logging.StreamHandler()
    ]
)

# Database file path
DB_NAME = 'untitled.db'

def create_database():
    """Creates the database with the required structure if it doesn't exist"""
    db_path = os.path.abspath(DB_NAME)
    
    # Check if database already exists
    if os.path.exists(db_path) and os.path.getsize(db_path) > 0:
        logging.info(f"Database already exists at {db_path}")
        return True
    
    logging.info(f"Creating new database at {db_path}")
    
    try:
        # Connect to the database (this will create it if it doesn't exist)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create Users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            username VARCHAR,
            password VARCHAR,
            division VARCHAR
        )
        ''')
        
        # Create index for Users table
        cursor.execute('CREATE INDEX IF NOT EXISTS index_id ON Users (id)')
        
        # Create tab_main_resp_server table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tab_main_resp_server (
            id_server INTEGER PRIMARY KEY,
            server_name VARCHAR UNIQUE,
            first_resp_person VARCHAR,
            second_resp_person VARCHAR,
            customer VARCHAR,
            system_name VARCHAR,
            project_name VARCHAR,
            operation_system VARCHAR,
            platform_name VARCHAR,
            addit_info VARCHAR
        )
        ''')
        
        # Create tab_collect_statistic table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tab_collect_statistic (
            gecos TEXT,
            home_dir TEXT,
            lastlog_user TEXT,
            supl_groups TEXT,
            user_name TEXT,
            server_name TEXT,
            date_entry TEXT,
            id_server VARCHAR,
            time_entry TEXT
        )
        ''')
        
        # Create tab_ao_resp table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tab_ao_resp (
            id_server INTEGER PRIMARY KEY,
            info_ao_resp BLOB
        )
        ''')
        
        conn.commit()
        conn.close()
        
        logging.info("Database created successfully with all required tables and indexes")
        return True
        
    except sqlite3.Error as e:
        logging.error(f"Error creating database: {e}")
        return False

if __name__ == "__main__":
    create_database()
