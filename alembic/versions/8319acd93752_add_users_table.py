"""add users table

Revision ID: 8319acd93752
Revises: f1a46a10d1a8
Create Date: 2022-02-23 08:19:55.003665

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8319acd93752'
down_revision = 'f1a46a10d1a8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    pass


def downgrade():
    op.drop_table('users')
    pass
