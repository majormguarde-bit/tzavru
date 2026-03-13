"""Add amenity resources and reservations

Revision ID: a2c4d7b9f012
Revises: e1bb9decab90
Create Date: 2026-03-14 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2c4d7b9f012'
down_revision = 'e1bb9decab90'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = set(inspector.get_table_names())
    existing_indexes = {}
    for table_name in ['amenity_resource', 'amenity_reservation']:
        if table_name in existing_tables:
            try:
                existing_indexes[table_name] = {idx['name'] for idx in inspector.get_indexes(table_name)}
            except Exception:
                existing_indexes[table_name] = set()

    if 'amenity_resource' not in existing_tables:
        op.create_table(
            'amenity_resource',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('property_id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(length=120), nullable=False),
            sa.Column('resource_type', sa.String(length=50), nullable=False),
            sa.Column('is_active', sa.Boolean(), server_default=sa.text('1'), nullable=False),
            sa.Column('slot_minutes', sa.Integer(), server_default='30', nullable=False),
            sa.Column('buffer_before_minutes', sa.Integer(), server_default='0', nullable=False),
            sa.Column('buffer_after_minutes', sa.Integer(), server_default='0', nullable=False),
            sa.Column('open_time', sa.Time(), server_default=sa.text("'08:00:00'"), nullable=False),
            sa.Column('close_time', sa.Time(), server_default=sa.text("'23:00:00'"), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['property_id'], ['property.id']),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_amenity_resource_property_id'), 'amenity_resource', ['property_id'], unique=False)
    else:
        ix_name = op.f('ix_amenity_resource_property_id')
        if ix_name not in existing_indexes.get('amenity_resource', set()):
            op.create_index(ix_name, 'amenity_resource', ['property_id'], unique=False)

    if 'amenity_reservation' not in existing_tables:
        op.create_table(
            'amenity_reservation',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('resource_id', sa.Integer(), nullable=False),
            sa.Column('booking_id', sa.Integer(), nullable=False),
            sa.Column('start_dt', sa.DateTime(), nullable=False),
            sa.Column('end_dt', sa.DateTime(), nullable=False),
            sa.Column('status', sa.String(length=20), server_default='requested', nullable=False),
            sa.Column('price_total', sa.Float(), server_default='0', nullable=False),
            sa.Column('notes', sa.Text(), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['booking_id'], ['booking.id']),
            sa.ForeignKeyConstraint(['resource_id'], ['amenity_resource.id']),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_amenity_reservation_booking_id'), 'amenity_reservation', ['booking_id'], unique=False)
        op.create_index(op.f('ix_amenity_reservation_end_dt'), 'amenity_reservation', ['end_dt'], unique=False)
        op.create_index(op.f('ix_amenity_reservation_resource_id'), 'amenity_reservation', ['resource_id'], unique=False)
        op.create_index(op.f('ix_amenity_reservation_start_dt'), 'amenity_reservation', ['start_dt'], unique=False)
    else:
        for ix_name, cols in [
            (op.f('ix_amenity_reservation_booking_id'), ['booking_id']),
            (op.f('ix_amenity_reservation_end_dt'), ['end_dt']),
            (op.f('ix_amenity_reservation_resource_id'), ['resource_id']),
            (op.f('ix_amenity_reservation_start_dt'), ['start_dt']),
        ]:
            if ix_name not in existing_indexes.get('amenity_reservation', set()):
                op.create_index(ix_name, 'amenity_reservation', cols, unique=False)


def downgrade():
    op.drop_index(op.f('ix_amenity_reservation_start_dt'), table_name='amenity_reservation')
    op.drop_index(op.f('ix_amenity_reservation_resource_id'), table_name='amenity_reservation')
    op.drop_index(op.f('ix_amenity_reservation_end_dt'), table_name='amenity_reservation')
    op.drop_index(op.f('ix_amenity_reservation_booking_id'), table_name='amenity_reservation')
    op.drop_table('amenity_reservation')

    op.drop_index(op.f('ix_amenity_resource_property_id'), table_name='amenity_resource')
    op.drop_table('amenity_resource')
