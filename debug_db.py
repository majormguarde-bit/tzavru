from flask import Flask
from config import Config
from database import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

from models import User

with app.app_context():
    print('Metadata tables:', db.metadata.tables.keys())
    db.create_all()
    
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    print('DB tables:', inspector.get_table_names())
