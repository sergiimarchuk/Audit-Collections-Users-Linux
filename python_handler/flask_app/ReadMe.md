# SQLite Database Explorer Flask App

A simple Flask application to explore and query SQLite databases.

## Setup Instructions

1. Install the required dependencies:
   ```bash
   pip install flask
   ```

2. Make sure the Flask app structure is set up correctly:
   ```
   flask_app/
   ├── app.py
   ├── README.md
   ├── static/
   │   └── css/
   │       └── style.css
   └── templates/
       ├── index.html
       └── report.html
   ```

3. The app is configured to look for the database at:
   `/opt/github_public_repo/Audit-Collections-Users-Linux/python_handler/_db/untitled.db`

## Running the Application

1. Navigate to the flask_app directory:
   ```bash
   cd /opt/github_public_repo/Audit-Collections-Users-Linux/python_handler/flask_app
   ```

2. Run the Flask application:
   ```bash
   python app.py
   ```

3. Access the application in your web browser:
   ```
   http://localhost:5000
   ```

## Features

- Simple homepage with a button to navigate to the reports page
- Reports page that lets you select and query tables from the SQLite database
- View up to 100 rows of data from any table
- Responsive design with Bootstrap styling

## Database Tables

The application connects to the `untitled.db` database which contains the following tables:
- Users
- tab_main_resp_server
- tab_collect_statistic
- tab_ao_resp
- report
