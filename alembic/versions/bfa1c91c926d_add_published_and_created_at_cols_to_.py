"""add published and created_at cols to posts table

Revision ID: bfa1c91c926d
Revises: de6533b174fc
Create Date: 2022-02-23 08:44:52.333547

"""
from http import server
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfa1c91c926d'
down_revision = 'de6533b174fc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(),
                  nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(
        timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('published')
    op.drop_column('created_at')
    pass
