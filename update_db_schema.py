from app import app, db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        inspector = db.inspect(db.engine)
        if inspector.has_table('property_options'):
            columns = [column['name'] for column in inspector.get_columns('property_options')]
            if 'price' not in columns:
                db.session.execute(db.text("ALTER TABLE property_options ADD COLUMN price FLOAT NOT NULL DEFAULT 0"))
                db.session.commit()
            if 'quantity' not in columns:
                db.session.execute(db.text("ALTER TABLE property_options ADD COLUMN quantity INTEGER NOT NULL DEFAULT 1"))
                db.session.commit()

        booking_option_table = None
        if inspector.has_table('booking_option'):
            booking_option_table = 'booking_option'
        elif inspector.has_table('booking_options'):
            booking_option_table = 'booking_options'

        if booking_option_table:
            booking_columns = [column['name'] for column in inspector.get_columns(booking_option_table)]
            if 'quantity' not in booking_columns:
                db.session.execute(db.text(f"ALTER TABLE {booking_option_table} ADD COLUMN quantity INTEGER NOT NULL DEFAULT 1"))
                db.session.commit()

        if inspector.has_table('option_type'):
            option_columns = [column['name'] for column in inspector.get_columns('option_type')]
            if 'price' not in option_columns:
                db.session.execute(db.text("ALTER TABLE option_type ADD COLUMN price FLOAT NOT NULL DEFAULT 0"))
                db.session.commit()
            if 'unit_type_id' not in option_columns:
                db.session.execute(db.text("ALTER TABLE option_type ADD COLUMN unit_type_id INTEGER"))
                db.session.commit()

        if inspector.has_table('characteristic_type'):
            characteristic_columns = [column['name'] for column in inspector.get_columns('characteristic_type')]
            if 'unit_type_id' not in characteristic_columns:
                db.session.execute(db.text("ALTER TABLE characteristic_type ADD COLUMN unit_type_id INTEGER"))
                db.session.commit()

        print("Database schema updated successfully!")
