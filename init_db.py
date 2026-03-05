from flask import Flask
from config import Config
from app import app, db
import os

def init_db():
    print("Инициализация базы данных...")
    
    # Убедимся, что папка instance существует
    base_dir = os.path.dirname(os.path.abspath(__file__))
    instance_dir = os.path.join(base_dir, 'instance')
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
        print(f"Создана папка: {instance_dir}")

    with app.app_context():
        # Показываем, куда будем писать
        print(f"Используемая база данных: {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        # Создаем все таблицы
        db.create_all()
        print('Все таблицы успешно созданы!')
        
        # Инструкция для миграций
        print("\nВАЖНО: Если вы используете миграции, выполните:")
        print("flask db stamp head")

if __name__ == "__main__":
    init_db()
