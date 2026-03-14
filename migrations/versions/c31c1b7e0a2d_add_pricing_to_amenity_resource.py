"""Add pricing to amenity resource

Revision ID: c31c1b7e0a2d
Revises: b7f0b4c2a1de
Create Date: 2026-03-14 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'c31c1b7e0a2d'
down_revision = 'b7f0b4c2a1de'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = set(inspector.get_table_names())

    if 'amenity_resource' not in existing_tables:
        return

    existing_columns = {c['name'] for c in inspector.get_columns('amenity_resource')}
    existing_indexes = {idx['name'] for idx in inspector.get_indexes('amenity_resource')}

    with op.batch_alter_table('amenity_resource') as batch_op:
        if 'price' not in existing_columns:
            batch_op.add_column(sa.Column('price', sa.Float(), nullable=False, server_default='0'))
        if 'unit_type_id' not in existing_columns:
            batch_op.add_column(sa.Column('unit_type_id', sa.Integer(), nullable=True))

    if op.f('ix_amenity_resource_unit_type_id') not in existing_indexes:
        op.create_index(op.f('ix_amenity_resource_unit_type_id'), 'amenity_resource', ['unit_type_id'], unique=False)


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = set(inspector.get_table_names())

    if 'amenity_resource' not in existing_tables:
        return

    existing_columns = {c['name'] for c in inspector.get_columns('amenity_resource')}

    try:
        op.drop_index(op.f('ix_amenity_resource_unit_type_id'), table_name='amenity_resource')
    except Exception:
        pass

    with op.batch_alter_table('amenity_resource') as batch_op:
        if 'unit_type_id' in existing_columns:
            batch_op.drop_column('unit_type_id')
        if 'price' in existing_columns:
            batch_op.drop_column('price')

