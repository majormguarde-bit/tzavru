"""Add amenity resource types

Revision ID: b7f0b4c2a1de
Revises: a2c4d7b9f012
Create Date: 2026-03-14 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'b7f0b4c2a1de'
down_revision = 'a2c4d7b9f012'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = set(inspector.get_table_names())

    existing_indexes = {}
    for table_name in ['amenity_resource', 'amenity_resource_type']:
        if table_name in existing_tables:
            try:
                existing_indexes[table_name] = {idx['name'] for idx in inspector.get_indexes(table_name)}
            except Exception:
                existing_indexes[table_name] = set()

    if 'amenity_resource_type' not in existing_tables:
        op.create_table(
            'amenity_resource_type',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(length=80), nullable=False),
            sa.Column('is_active', sa.Boolean(), server_default=sa.text('1'), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('name', name='uq_amenity_resource_type_name')
        )
    if op.f('ix_amenity_resource_type_name') not in existing_indexes.get('amenity_resource_type', set()):
        op.create_index(op.f('ix_amenity_resource_type_name'), 'amenity_resource_type', ['name'], unique=False)

    if 'amenity_resource' in existing_tables:
        amenity_resource_columns = {c['name'] for c in inspector.get_columns('amenity_resource')}
        if 'resource_type_id' not in amenity_resource_columns:
            op.add_column('amenity_resource', sa.Column('resource_type_id', sa.Integer(), nullable=True))

        if op.f('ix_amenity_resource_resource_type_id') not in existing_indexes.get('amenity_resource', set()):
            op.create_index(op.f('ix_amenity_resource_resource_type_id'), 'amenity_resource', ['resource_type_id'], unique=False)

        resource_types = [row[0] for row in bind.execute(sa.text(
            "SELECT DISTINCT resource_type FROM amenity_resource WHERE resource_type IS NOT NULL AND TRIM(resource_type) != ''"
        )).fetchall()]

        for name in resource_types:
            bind.execute(sa.text(
                "INSERT OR IGNORE INTO amenity_resource_type (name, is_active) VALUES (:name, 1)"
            ), {'name': name})

        bind.execute(sa.text(
            """
            UPDATE amenity_resource
            SET resource_type_id = (
                SELECT art.id
                FROM amenity_resource_type art
                WHERE art.name = amenity_resource.resource_type
                LIMIT 1
            )
            WHERE resource_type_id IS NULL
            """
        ))


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = set(inspector.get_table_names())

    if 'amenity_resource' in existing_tables:
        try:
            op.drop_index(op.f('ix_amenity_resource_resource_type_id'), table_name='amenity_resource')
        except Exception:
            pass
        try:
            with op.batch_alter_table('amenity_resource') as batch_op:
                batch_op.drop_column('resource_type_id')
        except Exception:
            pass

    if 'amenity_resource_type' in existing_tables:
        try:
            op.drop_index(op.f('ix_amenity_resource_type_name'), table_name='amenity_resource_type')
        except Exception:
            pass
        try:
            op.drop_table('amenity_resource_type')
        except Exception:
            pass
