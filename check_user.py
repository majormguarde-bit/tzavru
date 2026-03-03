from app import app, db, User
from werkzeug.security import check_password_hash

with app.app_context():
    users = User.query.all()
    print(f'Всего пользователей: {len(users)}')
    
    for user in users:
        print(f'Username: {user.username}')
        print(f'Email: {user.email}')
        print(f'Is admin: {user.is_admin}')
        print(f'Password hash: {user.password_hash[:50]}...')
        
        # Проверяем пароль
        is_valid = check_password_hash(user.password_hash, 'admin123')
        print(f'Password "admin123" valid: {is_valid}')
        print('---')
