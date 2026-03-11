"""add missing booking columns manually

Revision ID: 6eec914d9afe
Revises: 393075827ce4
Create Date: 2026-03-11 21:53:44.344645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6eec914d9afe'
down_revision = '393075827ce4'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.add_column(sa.Column('confirmation_code', sa.String(length=10), nullable=True))
        batch_op.add_column(sa.Column('is_email_confirmed', sa.Boolean(), nullable=True))


def downgrade():
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.drop_column('is_email_confirmed')
        batch_op.drop_column('confirmation_code')
