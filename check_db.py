import sqlite3
import os

db_path = os.path.join('instance', 'app.db')
if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(booking)")
    columns = [row[1] for row in cursor.fetchall()]
    print(f"Columns in {db_path}:")
    for col in columns:
        print(f"- {col}")
    conn.close()