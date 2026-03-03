from werkzeug.security import generate_password_hash
from app import app, db, User

with app.app_context():
    db.create_all()
    
    existing_admin = User.query.filter_by(username='admin').first()
    if existing_admin:
        print('Администратор уже существует')
    else:
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print('Администратор создан: admin/admin123')
