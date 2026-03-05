from werkzeug.security import generate_password_hash
from app import app, db, User
import sys

def create_admin_user():
    print("Создание администратора...")
    with app.app_context():
        # Сначала убедимся, что таблицы существуют
        db.create_all()
        
        # Проверяем, есть ли уже админ
        existing_admin = User.query.filter_by(username='admin').first()
        if existing_admin:
            print('Администратор "admin" уже существует.')
            print('Сброс пароля на "admin123"...')
            existing_admin.password_hash = generate_password_hash('admin123')
            db.session.commit()
            print('Пароль обновлен.')
        else:
            # Создаем нового админа
            admin = User(
                username='admin',
                email='admin@example.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print('Администратор создан успешно!')
            print('Логин: admin')
            print('Пароль: admin123')

if __name__ == "__main__":
    create_admin_user()
