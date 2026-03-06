import sqlite3
import os

db_path = 'instance/app.db'
print(f"Checking {db_path}...")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]
    
    for table in tables:
        if table == 'alembic_version': continue
        print(f"Table: {table}")
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        col_names = [c[1] for c in columns]
        print(f"  Columns: {col_names}")
        
    conn.close()
except Exception as e:
    print(f"Error: {e}")
