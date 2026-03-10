import os
from dotenv import load_dotenv

# Базовая директория приложения (где лежит config.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Загружаем .env из базовой директории
load_dotenv(os.path.join(BASE_DIR, '.env'))

class Config:
    BASE_DIR = BASE_DIR
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # Абсолютный путь к базе данных
    # Если DATABASE_URL не задан, используем локальный путь
    db_path = os.environ.get('DATABASE_URL')
    if not db_path:
        # Revert to app.db to restore data
        db_path = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'app.db')
    
    SQLALCHEMY_DATABASE_URI = db_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/uploads')
    MAX_CONTENT_LENGTH = 128 * 1024 * 1024  # 128MB max-limit

    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    # Web Push VAPID keys
    VAPID_PUBLIC_KEY = os.environ.get('VAPID_PUBLIC_KEY')
    VAPID_PRIVATE_KEY = os.environ.get('VAPID_PRIVATE_KEY')
    VAPID_CLAIM_EMAIL = os.environ.get('VAPID_CLAIM_EMAIL', 'admin@imperial-collection.ru')
    
    # WebAuthn settings
    WEBAUTHN_RP_ID = os.environ.get('WEBAUTHN_RP_ID')
    WEBAUTHN_RP_NAME = os.environ.get('WEBAUTHN_RP_NAME', 'Imperial Collection')
    WEBAUTHN_ORIGIN = os.environ.get('WEBAUTHN_ORIGIN')
