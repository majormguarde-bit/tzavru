from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import Config
import json
from functools import wraps

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = 'dev-secret-key-change-this-in-production'

db = SQLAlchemy(app)

# Добавляем фильтры для Jinja2
@app.template_filter('from_json')
def from_json(value):
    if isinstance(value, str):
        try:
            return json.loads(value)
        except:
            return []
    return value

@app.template_filter('format_price')
def format_price(value):
    try:
        return f"{int(value):,}".replace(',', ' ')
    except:
        return value

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    property_type = db.Column(db.String(50), nullable=False)
    short_description = db.Column(db.String(200), nullable=False)
    full_description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(300))
    gallery_urls = db.Column(db.Text)
    price_per_night = db.Column(db.Float, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    amenities = db.Column(db.Text)
    features = db.Column(db.Text)
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    guest_name = db.Column(db.String(100), nullable=False)
    guest_email = db.Column(db.String(120), nullable=False)
    guest_phone = db.Column(db.String(20), nullable=False)
    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)
    guests_count = db.Column(db.Integer, nullable=False)
    special_requests = db.Column(db.Text)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    property = db.relationship('Property', backref=db.backref('bookings', lazy=True))

class ContactRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_processed = db.Column(db.Boolean, default=False)

# Простой декоратор для проверки авторизации
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Требуется авторизация', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Требуется авторизация', 'error')
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            flash('Требуются права администратора', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    properties = Property.query.order_by(Property.created_at.desc()).all()
    return render_template('index.html', properties=properties)

@app.route('/property/<int:id>')
def property_detail(id):
    property = Property.query.get_or_404(id)
    return render_template('property_detail.html', property=property)

@app.route('/booking/<int:property_id>', methods=['GET', 'POST'])
def booking(property_id):
    if request.method == 'POST':
        booking = Booking(
            property_id=property_id,
            guest_name=request.form['guest_name'],
            guest_email=request.form['guest_email'],
            guest_phone=request.form.get('guest_phone', ''),
            check_in=request.form['check_in'],
            check_out=request.form['check_out'],
            guests_count=int(request.form.get('guests_count', 1)),
            total_price=float(request.form.get('total_price', 0))
        )
        db.session.add(booking)
        db.session.commit()
        flash('Бронирование отправлено!', 'success')
        return redirect(url_for('index'))
    return render_template('booking.html', property_id=property_id)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        contact = ContactRequest(
            name=request.form['name'],
            email=request.form['email'],
            phone=request.form.get('phone', ''),
            message=request.form['message']
        )
        db.session.add(contact)
        db.session.commit()
        flash('Сообщение отправлено!', 'success')
        return redirect(url_for('index'))
    return render_template('base.html')

# Admin routes
@app.route('/admin')
@admin_required
def admin_dashboard():
    properties = Property.query.count()
    bookings = Booking.query.count()
    contacts = ContactRequest.query.count()
    return render_template('admin/dashboard.html', properties=properties, bookings=bookings, contacts=contacts)

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        from werkzeug.security import check_password_hash
        username = request.form.get('username')
        password = request.form.get('password')
        
        print(f'Login attempt - Username: {username}, Password: {password}')
        
        user = User.query.filter_by(username=username).first()
        print(f'User found: {user is not None}')
        
        if user:
            print(f'User is_admin: {user.is_admin}')
            is_valid = check_password_hash(user.password_hash, password)
            print(f'Password valid: {is_valid}')
            
            if is_valid:
                # Простая сессия вместо Flask-Login
                session['user_id'] = user.id
                session['username'] = user.username
                session['is_admin'] = user.is_admin
                print(f'Session set: user_id={user.id}, username={user.username}')
                flash('Вход выполнен успешно', 'success')
                return redirect(url_for('admin_dashboard'))
        
        flash('Неверные учетные данные', 'error')
    return render_template('admin/login.html')

@app.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin/properties')
@login_required
def admin_properties():
    properties = Property.query.all()
    return render_template('admin/properties.html', properties=properties)

@app.route('/admin/properties/add', methods=['GET', 'POST'])
@login_required
def add_property():
    if request.method == 'POST':
        # Преобразуем amenities и features в JSON
        amenities = request.form.get('amenities', '').strip().split('\n')
        amenities = [a.strip() for a in amenities if a.strip()]
        
        features = request.form.get('features', '').strip().split('\n')
        features = [f.strip() for f in features if f.strip()]
        
        property = Property(
            name=request.form['name'],
            property_type=request.form['property_type'],
            short_description=request.form['short_description'],
            full_description=request.form['full_description'],
            location=request.form['location'],
            image_url=request.form['image_url'],
            price_per_night=float(request.form['price_per_night']),
            capacity=int(request.form['capacity']),
            amenities=json.dumps(amenities),
            features=json.dumps(features)
        )
        db.session.add(property)
        db.session.commit()
        flash('Объект добавлен', 'success')
        return redirect(url_for('admin_properties'))
    return render_template('admin/edit_property.html')

@app.route('/admin/bookings')
@login_required
def admin_bookings():
    bookings = Booking.query.all()
    return render_template('admin/bookings.html', bookings=bookings)

@app.route('/admin/contacts')
@login_required
def admin_contacts():
    contacts = ContactRequest.query.all()
    return render_template('admin/contacts.html', contacts=contacts)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
