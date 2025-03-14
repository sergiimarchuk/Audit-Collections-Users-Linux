#!/usr/bin/python
"""
This script parses files with names starting with 'local_report' and imports user data 
into a SQLite database. It processes information about users from /etc/passwd and lastlog.
"""
from collections import Counter
import datetime
import sqlite3
import glob
import os
import ast
import logging

# Set up logging to both console and file
log_file = "user_data_import.log"
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
DB_NAME = '../_db/untitled.db'  # Using original database name
REPORT_PREFIX = 'local_report'

# Current directory path
current_dir = os.getcwd()
# Get the parent directory (one level up)
parent_dir = os.path.dirname(current_dir)

# Add the target directory (_data) to the parent directory
target_dir = os.path.join(parent_dir, "_data")


# Connect to database
def connect_to_db():
    db_path = os.path.join(current_dir, DB_NAME)
    
    # Check if the database file exists and has content
    if not os.path.exists(db_path) or os.path.getsize(db_path) == 0:
        logging.error(f" ! Database file does not exist or is empty: {db_path}  N. B. !: Please create db manually, just run python script which is located in dir {target_dir} with name creation_db_untitled.py")
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

def sql_get_id_server(server_name):
    """Get server ID from the server name - keeping original function name and query."""
    try:
        cursor.execute("""SELECT "id_server" FROM "tab_main_resp_server" WHERE "server_name" = ?""", (server_name,))
        row = cursor.fetchall()
        return row
    except sqlite3.Error as e:
        logging.error(f"Error retrieving server ID: {e}")
        return []

def sqlupdate(id_server, gecos, home_dir, lastlog_user, supl_groups, user_name, server_name, date_entry, time_entry):
    """Insert user data into the database - keeping original function name and parameters."""
    try:
        cursor.execute('INSERT INTO tab_collect_statistic(id_server, gecos, home_dir, lastlog_user, supl_groups, user_name, server_name, date_entry, time_entry) \
        VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ? )', (id_server, gecos, home_dir, lastlog_user, supl_groups, user_name, server_name, date_entry, time_entry))
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Error inserting data: {e}")
        conn.rollback()

def get_info():
    """Process all report files in the current directory - keeping original function name."""
    files_processed = 0
    records_added = 0
    
    files_in_dir = os.listdir(target_dir)
    for files in files_in_dir:
        #print(files)
        if "local_report" in files:
            try:
                # Extract server name from filename - keeping original logic
                #print(files)
                print(target_dir,files)
                try:
                    server_name = files.split("local_report_")[1]
                    print("server name is:", server_name,)
                except IndexError:
                    server_name = "local"
                
                logging.info(f"Processing file: {files} for server: {server_name}") # sure that is correct 
                print("files anme are: ", files)
                with open(os.path.join(target_dir, files), "r") as fp:
                    for lines in fp:
                        try:
                            # Parse line - keeping original parsing approach
                            data = ast.literal_eval(lines)
                            user_name = data.get("user_name")
                            gecos = data.get("gecos")
                            supl_groups = data.get("supplementary_groups")
                            home_dir = data.get("home_directory")
                            lastlog_user = data.get("lastlog")
                            date_file = data.get("date_checking")
                            time_entry = data.get("time_checking")
                            
                            # CRITICAL CHANGE: Using original logic - checking server_name length, not result of sql_get_id_server
                            if len((server_name)) > 0:
                                sqlupdate(server_name, gecos, home_dir, str(lastlog_user), str(supl_groups), 
                                         user_name, server_name, date_file, time_entry)
                                records_added += 1
                        except (SyntaxError, ValueError) as e:
                            logging.error(f"Error parsing line in {files}: {e}")
                            continue
                
                files_processed += 1
                
            except Exception as e:
                logging.error(f"Error processing file {files}: {e}")
                continue
    
    logging.info(f"Processing complete. Files processed: {files_processed}, Records added: {records_added}")

if __name__ == "__main__":
    conn, cursor, status = connect_to_db()
    get_info()
    if status:
        print(status)
        try:
            pass
        finally:
            conn.close()
            logging.info("Database connection closed")
    else:
        # DB connection failed, the error is already logged in connect_to_db()
        # No need to do anything else
        pass
            

    logging.info("Script execution completed")