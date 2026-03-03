from app import app, db, User
from werkzeug.security import check_password_hash
from flask import request

with app.app_context():
    # Создаём тестового пользователя
    test_user = User.query.filter_by(username='test').first()
    if not test_user:
        from werkzeug.security import generate_password_hash
        test_user = User(
            username='test',
            email='test@example.com',
            password_hash=generate_password_hash('test123'),
            is_admin=False
        )
        db.session.add(test_user)
        db.session.commit()
        print('Test user created: test/test123')
    
    # Тестируем логин
    print('\nTesting login...')
    
    # Имитируем запрос
    with app.test_request_context(method='POST', data={'username': 'admin', 'password': 'admin123'}):
        from werkzeug.security import check_password_hash
        username = request.form.get('username')
        password = request.form.get('password')
        
        print(f'Username from form: {username}')
        print(f'Password from form: {password}')
        
        user = User.query.filter_by(username=username).first()
        print(f'User found: {user.username if user else "None"}')
        
        if user:
            is_valid = check_password_hash(user.password_hash, password)
            print(f'Password valid: {is_valid}')
            
            if is_valid:
                print('Login would be successful')
            else:
                print('Password invalid')
        else:
            print('User not found')
    
    print('\nTesting with wrong password...')
    with app.test_request_context(method='POST', data={'username': 'admin', 'password': 'wrong'}):
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user:
            is_valid = check_password_hash(user.password_hash, password)
            print(f'Password valid: {is_valid}')