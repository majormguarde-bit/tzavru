from flask import Flask
from config import Config
from database import db

app = Flask(__name__)
app.config.from_object(Config)
print('DB URI:', app.config['SQLALCHEMY_DATABASE_URI'])
db.init_app(app)

from models import User, Property, Booking, ContactRequest

with app.app_context():
    print('Creating tables...')
    db.create_all()
    print('Tables created')
    
    # Проверяем таблицы
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print('Tables in database:', tables)
