import sqlite3

conn = sqlite3.connect('instance/app.db')
cursor = conn.cursor()

# Проверяем, существует ли admin
cursor.execute("SELECT * FROM user WHERE username = 'admin'")
if cursor.fetchone():
    print('Администратор уже существует')
else:
    cursor.execute("""
        INSERT INTO user (username, email, password_hash, is_admin) 
        VALUES ('admin', 'admin@example.com', 
        'scrypt:32768:8:1$LJ6aQKL4HZ44jM7E$587a88e32e52e15ece41adf7626f899735ceb8d27375d4fbe5ce9e2ae0bdd776418ba3964f3d732794cb0a129b8e0b447ac52f3894a025dc23099bc78edb9730', 
        1)
    """)
    conn.commit()
    print('Администратор создан: admin/admin123')

conn.close()
