import sqlite3
import os

# Database file path
db_path = 'untitled.db'  # Change this to the full path if needed

def get_db_structure():
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("Extracting database structure for:", db_path)
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("\n=== Tables ===")
        for table in tables:
            table_name = table[0]
            print(f"\nTable: {table_name}")
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print("Columns:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]}){' PRIMARY KEY' if col[5] else ''}")
            
            # Get table indexes
            cursor.execute(f"PRAGMA index_list({table_name})")
            indexes = cursor.fetchall()
            if indexes:
                print("Indexes:")
                for idx in indexes:
                    index_name = idx[1]
                    print(f"  - {index_name}")
                    # Get index columns
                    cursor.execute(f"PRAGMA index_info({index_name})")
                    idx_columns = cursor.fetchall()
                    print(f"    Columns: {', '.join(c[2] for c in idx_columns)}")
            
            # Get foreign keys
            cursor.execute(f"PRAGMA foreign_key_list({table_name})")
            fkeys = cursor.fetchall()
            if fkeys:
                print("Foreign Keys:")
                for fk in fkeys:
                    print(f"  - {fk[3]} -> {fk[2]}.{fk[4]}")
        
        # Get views
        cursor.execute("SELECT name FROM sqlite_master WHERE type='view';")
        views = cursor.fetchall()
        if views:
            print("\n=== Views ===")
            for view in views:
                view_name = view[0]
                print(f"\nView: {view_name}")
                # Get view definition
                cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='view' AND name='{view_name}';")
                view_def = cursor.fetchone()
                print(f"Definition: {view_def[0]}")
        
        # Get triggers
        cursor.execute("SELECT name FROM sqlite_master WHERE type='trigger';")
        triggers = cursor.fetchall()
        if triggers:
            print("\n=== Triggers ===")
            for trigger in triggers:
                trigger_name = trigger[0]
                print(f"\nTrigger: {trigger_name}")
                # Get trigger definition
                cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='trigger' AND name='{trigger_name}';")
                trigger_def = cursor.fetchone()
                print(f"Definition: {trigger_def[0]}")
        
        conn.close()
        print("\nDatabase structure extraction complete.")
        
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_db_structure()
