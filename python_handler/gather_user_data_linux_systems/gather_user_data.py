#!/usr/bin/python3
import socket
import subprocess
import os
import json
from datetime import datetime

#!/usr/bin/python
import socket
import subprocess
import os
import shutil
from datetime import datetime

formatted_time = datetime.now().strftime("_moved_%Y-%m-%dt%Hh%Mm%Ss")

hostname_var = socket.gethostname()


dict_user_var = {}

new_dict = {}

group_list = []

# Get timestamp
datetime_var = datetime.now().strftime('%Y-%m-%d')
time_var = datetime.now().strftime('%H:%M:%S')

# Get hostname
hostname_var = socket.gethostname()

# Log file
checklog_file_ = "local_report_"

# Dictionary to store user data
users_data = {}

# Get current working directory
cwd = os.getcwd()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # l # o # g # i # n # g # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import logging

def setup_logger(log_file="log_gathering.log", level=logging.INFO):
    logging.basicConfig(
        filename=log_file,
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def log_message(message, level="info"):
    levels = {
        "debug": logging.debug,
        "info": logging.info,
        "warning": logging.warning,
        "error": logging.error,
        "critical": logging.critical
    }
    levels.get(level.lower(), logging.info)(message)

# Example Usage
setup_logger()
#log_message("This is an info message.")
#log_message("This is a warning!", "warning")
#log_message("An error occurred!", "error")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def log_rm():
    """Remove log file if it exists."""
    if os.path.isfile(f"{cwd}/data/{checklog_file_}"):
        os.remove(f"{cwd}/data/{checklog_file_}")
        print('old one file with data has been deleted')

#log_rm()

def log_rm_ex(file_path, archive_dir='/tmp'):
    """Move log file to archive directory with timestamp."""
    import os
    import shutil
    from datetime import datetime

    file_name = os.path.basename(file_path)

    if os.path.isfile(file_path):
        archive_path = os.path.join(archive_dir, f"{file_name}_{formatted_time}")
        shutil.move(file_path, archive_path)
        message_filelog = (f"File: {file_name} has been moved to: {archive_path}. Original source: {cwd}")
        log_message(message_filelog)
        return True
    else:
        print(f"File {file_name} does not exist")
        
        return False

log_rm_ex(checklog_file_)

def checklog_file(content):
    """Append content to log file."""
    with open(os.path.join(cwd, checklog_file_), 'a') as f:
        f.write(content + '\n')

def run_ext_bin(cmd, arg1, arg2):
    """Run an external command and return output."""
    try:
        result = subprocess.run([cmd, arg1, arg2], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        
        return result.stdout.split()[-6:]
    except subprocess.CalledProcessError as e:
        return f"Error running {cmd}: {e}"
    
    
def read_dic(dict_data):
    """Format and log a user data dictionary."""
    if isinstance(dict_data, dict):  # Check if value is a dictionary
        dict_str = ", ".join(f"{k}: {v}" for k, v in dict_data.items())
        checklog_file(dict_str)
    else:
        print('Error issue with dict for collection user data')

def extract_groups():
    """Extract user and group details from /etc/passwd."""
    with open("/etc/passwd", "r") as fp:
        for user_line in fp:
            user_data = {}
            user_parts = user_line.strip().split(":")
            username = user_parts[0]
            home_directory = user_parts[5]
            gecos_field = user_parts[4] if len(user_parts[4]) >= 3 else "GECOS IS EMPTY"

            try:
                # Get user ID details
                run_cmd_id = subprocess.run(['id', username], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
                output_cmd_id_str = run_cmd_id.stdout

                # Extract username
                uname_var = output_cmd_id_str.split(" ")[0].split("(")[1].replace(")", "")

                # Extract primary group
                primary_group_raw = output_cmd_id_str.split(" ")[1].split("=")[1]
                primary_group = primary_group_raw.split("(")[1].replace(")", "")

                # Extract supplementary groups
                groups_raw = output_cmd_id_str.split(" ")[2].split("=")[1]
                supplementary_groups = [grp.split("(")[1].replace(")", "") for grp in groups_raw.split(",") if grp]

                # Extract last login information
                last_log_user_var = run_ext_bin("lastlog", "-u", uname_var)
                
                if "Never" in str(last_log_user_var):
                    last_log_user_var = "Never logged in"
                else:
                    try:
                        log_month = last_log_user_var[1] if last_log_user_var[1] else last_log_user_var[0]
                        log_day = last_log_user_var[2]
                        log_year = last_log_user_var[5]
                        last_log_user_var = f"{log_day}/{log_month}/{log_year}"
                    except IndexError:
                        last_log_user_var = "Unknown last login format"

                # Store user info
                user_data = {
                    'date_checking': datetime_var,
                    'time_checking': time_var,                     
                    'hostname':hostname_var,
                    'user_name': uname_var,
                    'primary_group': primary_group,
                    'supplementary_groups': supplementary_groups,
                    'home_directory': home_directory,
                    'gecos': gecos_field,
                    'lastlog': last_log_user_var                    
                }

                # Save to main dictionary
                users_data[username] = user_data
                
                # Log only if "COMPANYNAME" is not in gecos_field
                if "COMPANYNAME" not in gecos_field:
                    checklog_file(str(user_data)) #!!! do not delete this line it is works as expected just for special case without function read_dic(dict_data)
                    #read_dic(user_data) #this works as expected just without at the begining line \{ and at the end line \} so we can use script without extra function read_dic(dict_data) in this case less code in this script 

            except (IndexError, AttributeError, subprocess.CalledProcessError) as e:
                print(f"Error processing user {username}: {e}")
                error_message = (f"Error processing user {username}: {e}")
               
                

extract_groups()

def prep_to_excel():
    """Read the log file for Excel preparation."""
    with open(f"{cwd}/{checklog_file_}", "r") as fc:
        for dic_line in fc:
            print(dic_line.strip())            






