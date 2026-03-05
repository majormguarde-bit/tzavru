import os
from app import app, db

def fix_db():
    # Ensure instance directory exists
    base_dir = os.path.dirname(os.path.abspath(__file__))
    instance_dir = os.path.join(base_dir, 'instance')
    
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
        print(f"Created directory: {instance_dir}")

    with app.app_context():
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        print(f"Connecting to database: {db_uri}")
        
        print("Creating all missing tables...")
        db.create_all()
        print("Tables created successfully!")
        print("\nNow run this command to mark migrations as done:")
        print("flask db stamp head")

if __name__ == "__main__":
    fix_db()
