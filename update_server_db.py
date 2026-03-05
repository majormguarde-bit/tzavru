
import sqlite3
import os

def migrate_db(db_path):
    print(f"Checking database at: {db_path}")
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    migrations = [
        # Table, Column, Type, Default
        ('review', 'title', 'VARCHAR(200)', None),
        ('review', 'author', 'VARCHAR(100)', None),
        ('review', 'avatar_url', 'VARCHAR(300)', None),
        ('user', 'phone', 'VARCHAR(20)', None),
        ('site_settings', 'favicon_url', 'VARCHAR(300)', None),
        ('site_settings', 'slogan', 'VARCHAR(300)', "Три грани настоящего отдыха в Псковской области"),
        ('site_settings', 'map_url', 'TEXT', None),
        ('property', 'latitude', 'FLOAT', None),
        ('property', 'longitude', 'FLOAT', None),
        ('contact_request', 'message', 'TEXT', "")
    ]

    for table, column, col_type, default in migrations:
        try:
            # Check if table exists
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if not cursor.fetchone():
                print(f"Table '{table}' does not exist, skipping.")
                continue

            cursor.execute(f"PRAGMA table_info({table})")
            columns = [col[1] for col in cursor.fetchall()]
            
            if column not in columns:
                print(f"Adding column '{column}' to table '{table}'...")
                alter_query = f"ALTER TABLE {table} ADD COLUMN {column} {col_type}"
                if default is not None:
                    # SQLite allows DEFAULT in ADD COLUMN
                    if isinstance(default, str):
                        alter_query += f" DEFAULT '{default}'"
                    else:
                        alter_query += f" DEFAULT {default}"
                
                cursor.execute(alter_query)
                conn.commit()
                print(f"Successfully added '{column}'.")
            else:
                print(f"Column '{column}' already exists in '{table}'.")
                
        except sqlite3.Error as e:
            print(f"Error migrating {table}.{column}: {e}")

    conn.close()

if __name__ == "__main__":
    # Check both potential database locations
    db_paths = [
        'instance/imperial.db',
        'instance/app.db',
        'app.db',
        'imperial.db'
    ]
    
    found = False
    for path in db_paths:
        if os.path.exists(path):
            migrate_db(path)
            found = True
            
    if not found:
        print("No database files found in standard locations.")
    else:
        print("Migration completed.")
