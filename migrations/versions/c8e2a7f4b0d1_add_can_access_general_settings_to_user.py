"""Add can_access_general_settings to user

Revision ID: c8e2a7f4b0d1
Revises: 9f2c1f0a7b1e
Create Date: 2026-03-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'c8e2a7f4b0d1'
down_revision = '9f2c1f0a7b1e'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = set(inspector.get_table_names())

    if 'user' not in existing_tables:
        return

    cols = {c['name'] for c in inspector.get_columns('user')}
    if 'can_access_general_settings' not in cols:
        op.add_column('user', sa.Column('can_access_general_settings', sa.Boolean(), server_default=sa.text('0'), nullable=True))
        op.execute("UPDATE user SET can_access_general_settings = 0 WHERE can_access_general_settings IS NULL")


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = set(inspector.get_table_names())

    if 'user' not in existing_tables:
        return

    cols = {c['name'] for c in inspector.get_columns('user')}
    if 'can_access_general_settings' in cols:
        op.drop_column('user', 'can_access_general_settings')
