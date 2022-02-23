"""add content column to post table

Revision ID: f1a46a10d1a8
Revises: 5ed5c67b46c8
Create Date: 2022-02-22 23:37:34.491311

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1a46a10d1a8'
down_revision = '5ed5c67b46c8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts', sa.Column('content', sa.String(), nullable=False)
    )
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
