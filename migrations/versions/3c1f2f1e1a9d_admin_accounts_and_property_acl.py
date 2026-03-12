"""admin accounts and property acl

Revision ID: 3c1f2f1e1a9d
Revises: 6eec914d9afe
Create Date: 2026-03-12

"""

from alembic import op
import sqlalchemy as sa


revision = '3c1f2f1e1a9d'
down_revision = '6eec914d9afe'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    op.execute("DROP TABLE IF EXISTS _alembic_tmp_user")
    op.execute("DROP TABLE IF EXISTS _alembic_tmp_property")

    table_names = set(inspector.get_table_names())

    if 'user' in table_names:
        user_columns = {c['name'] for c in inspector.get_columns('user')}
        missing_user_columns = [
            ('is_superadmin', sa.Column('is_superadmin', sa.Boolean(), nullable=False, server_default=sa.text('0'))),
            ('can_create_properties', sa.Column('can_create_properties', sa.Boolean(), nullable=False, server_default=sa.text('1'))),
            ('can_edit_properties', sa.Column('can_edit_properties', sa.Boolean(), nullable=False, server_default=sa.text('1'))),
            ('can_delete_properties', sa.Column('can_delete_properties', sa.Boolean(), nullable=False, server_default=sa.text('1'))),
        ]
        user_cols_to_add = [col for name, col in missing_user_columns if name not in user_columns]
        if user_cols_to_add:
            with op.batch_alter_table('user', schema=None) as batch_op:
                for col in user_cols_to_add:
                    batch_op.add_column(col)

    if 'property' in table_names:
        property_columns = {c['name'] for c in inspector.get_columns('property')}
        property_indexes = inspector.get_indexes('property')
        property_foreign_keys = inspector.get_foreign_keys('property')

        needs_owner_id = 'owner_id' not in property_columns
        needs_owner_idx = not any(ix.get('column_names') == ['owner_id'] for ix in property_indexes)
        needs_owner_fk = not any(
            fk.get('referred_table') == 'user' and fk.get('constrained_columns') == ['owner_id']
            for fk in property_foreign_keys
        )

        if needs_owner_id or needs_owner_idx or needs_owner_fk:
            with op.batch_alter_table('property', schema=None) as batch_op:
                if needs_owner_id:
                    batch_op.add_column(sa.Column('owner_id', sa.Integer(), nullable=True))
                if needs_owner_idx:
                    batch_op.create_index(batch_op.f('ix_property_owner_id'), ['owner_id'], unique=False)
                if needs_owner_fk:
                    batch_op.create_foreign_key('fk_property_owner_id_user', 'user', ['owner_id'], ['id'])

    if 'admin_property_access' not in table_names:
        op.create_table(
            'admin_property_access',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False, index=True),
            sa.Column('property_id', sa.Integer(), sa.ForeignKey('property.id'), nullable=False, index=True),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.UniqueConstraint('user_id', 'property_id', name='uq_admin_property_access_user_property')
        )

    inspector = sa.inspect(conn)
    table_names = set(inspector.get_table_names())
    user_columns = {c['name'] for c in inspector.get_columns('user')} if 'user' in table_names else set()
    property_columns = {c['name'] for c in inspector.get_columns('property')} if 'property' in table_names else set()

    superadmin_id = conn.execute(sa.text("SELECT id FROM user WHERE is_admin = 1 ORDER BY id ASC LIMIT 1")).scalar()
    if superadmin_id:
        if 'is_superadmin' in user_columns:
            conn.execute(sa.text("UPDATE user SET is_superadmin = 1 WHERE id = :id"), {"id": superadmin_id})
        if 'owner_id' in property_columns:
            conn.execute(sa.text("UPDATE property SET owner_id = :id WHERE owner_id IS NULL"), {"id": superadmin_id})


def downgrade():
    op.drop_table('admin_property_access')

    with op.batch_alter_table('property', schema=None) as batch_op:
        batch_op.drop_constraint('fk_property_owner_id_user', type_='foreignkey')
        batch_op.drop_index(batch_op.f('ix_property_owner_id'))
        batch_op.drop_column('owner_id')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('can_delete_properties')
        batch_op.drop_column('can_edit_properties')
        batch_op.drop_column('can_create_properties')
        batch_op.drop_column('is_superadmin')
