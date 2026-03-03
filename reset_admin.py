from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Удаляем старого admin
    old_admin = User.query.filter_by(username='admin').first()
    if old_admin:
        db.session.delete(old_admin)
        db.session.commit()
        print('Старый admin удалён')
    
    # Создаём нового
    admin = User(
        username='admin',
        email='admin@example.com',
        password_hash=generate_password_hash('admin123'),
        is_admin=True
    )
    db.session.add(admin)
    db.session.commit()
    print('Новый admin создан: admin/admin123')
    
    # Проверяем
    user = User.query.filter_by(username='admin').first()
    print(f'Проверка: username={user.username}, is_admin={user.is_admin}')
    print(f'Password hash: {user.password_hash[:50]}...')