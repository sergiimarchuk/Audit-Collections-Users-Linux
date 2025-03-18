# app.py
from flask import Flask, render_template, request, jsonify
import sqlite3
import os
import sys

app = Flask(__name__)

# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '_db', 'untitled.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/api/tables')
def get_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get list of tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return jsonify(tables)

@app.route('/api/query', methods=['POST'])
def query_data():
    data = request.json
    table_name = data.get('table_name')
    
    if not table_name:
        return jsonify({'error': 'No table name provided'}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [row[1] for row in cursor.fetchall()]
        
        # Get data (limit to 100 rows for safety)
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 100;")
        rows = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return jsonify({
            'columns': columns,
            'rows': rows
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Ensure the database path is correct
    if not os.path.exists(DB_PATH):
        print(f"Database not found at: {DB_PATH}")
        sys.exit(1)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
