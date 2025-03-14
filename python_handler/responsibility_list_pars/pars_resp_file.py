#!/usr/bin/python
"""
This script imports server responsibility information from a text file
and updates a SQLite database. It checks if servers already exist
in the database before adding them.
"""
from __future__ import print_function  
import datetime
import sqlite3
import os
import logging

# Set up logging to both console and file
log_file = "server_responsibility_import.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),  # Write to file
        logging.StreamHandler()         # Write to console
    ]
)
logging.info("Starting script execution")

# Configuration
DB_NAME = '../_db/untitled.db'
RESPONSIBILITY_FILE = 'responsibility-list.txt'

# Get current directory path
current_dir = os.getcwd()
logging.info("Working directory: %s" % current_dir)

# Connect to database
def connect_to_db():
    db_path = os.path.join(current_dir, DB_NAME)
    
    # Check if the database file exists and has content
    if not os.path.exists(db_path) or os.path.getsize(db_path) == 0:
        logging.error(f"Database file does not exist or is empty: {db_path}")
        return None, None, False
        
    try:
        conn = sqlite3.connect(db_path)
        conn.text_factory = str
        cursor = conn.cursor()
        logging.info(f"Connected to database: {DB_NAME}")
        return conn, cursor, True
    except sqlite3.Error as e:
        logging.error(f"Database connection error: {e}")
        return None, None, False
        
def add_server_to_db(addit_info, customer, first_resp_person, operation_system, 
                     platform_name, project_name, second_resp_person, server_name, system_name):
    """Insert server responsibility data into the database"""
    try:
        cursor.execute('''
            INSERT INTO tab_main_resp_server(
                addit_info, customer, first_resp_person, operation_system, 
                platform_name, project_name, second_resp_person, server_name, system_name
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (addit_info, customer, first_resp_person, operation_system, 
              platform_name, project_name, second_resp_person, server_name, system_name))
        conn.commit()
        logging.info("Added server %s to database" % server_name)
        return True
    except sqlite3.Error as e:
        logging.error("Error inserting data for server %s: %s" % (server_name, e))
        conn.rollback()
        return False

def check_server_exists(server_name):
    """Check if a server already exists in the database"""
    try:
        cursor.execute("SELECT COUNT(*) FROM tab_main_resp_server WHERE server_name = ?", (server_name,))
        count = cursor.fetchone()[0]
        return count > 0
    except sqlite3.Error as e:
        logging.error("Error checking if server %s exists: %s" % (server_name, e))
        return False

def process_responsibility_file():
    """Process the responsibility list file and update the database"""
    file_path = os.path.join(current_dir, RESPONSIBILITY_FILE)
    servers_processed = 0
    servers_added = 0
    
    try:
        with open(file_path, "r") as fp:  
            for line_number, line in enumerate(fp, 1):
                try:
                    # Split the line into fields
                    fields = line.strip().split(":")
                    
                    if len(fields) < 8:
                        logging.warning("Line %d has insufficient fields: %s" % (line_number, line.strip()))
                        continue
                    
                    server_name = fields[0].strip()
                    first_resp_person = fields[1].strip()
                    second_resp_person = fields[2].strip()
                    customer = fields[3].strip()
                    system_name = fields[4].strip()
                    project_name = fields[5].strip()
                    operation_system = fields[6].strip()
                    platform_name = fields[7].strip()
                    addit_info = ""  # Additional info field is empty by default
                    
                    logging.info("Processing server: %s" % server_name)
                    print("Processing server from file:", server_name)  # Similar to original script's output
                    servers_processed += 1
                    
                    # Check if server already exists in database
                    if not check_server_exists(server_name):
                        # Add server to database
                        success = add_server_to_db(
                            addit_info, customer, first_resp_person, operation_system,
                            platform_name, project_name, second_resp_person, server_name, system_name
                        )
                        if success:
                            servers_added += 1
                    else:
                        logging.info("Server %s already exists in database, skipping" % server_name)
                        
                except Exception as e:
                    logging.error("Error processing line %d: %s" % (line_number, e))
                    continue
                    
        logging.info("Processing complete. Servers processed: %d, Servers added: %d" % 
                    (servers_processed, servers_added))
        
    except IOError:  # 
        logging.error("Responsibility file not found: %s" % file_path)
    except Exception as e:
        logging.error("Error processing responsibility file: %s" % e)

if __name__ == "__main__":
    conn, cursor, status = connect_to_db()
    
    if status:
        print(status)
        try:
            process_responsibility_file()
            #pass
        finally:
            conn.close()
            logging.info("Database connection closed")
    else:
        # DB connection failed, the error is already logged in connect_to_db()
        # No need to do anything else
        pass
            
    logging.info("Script execution completed")