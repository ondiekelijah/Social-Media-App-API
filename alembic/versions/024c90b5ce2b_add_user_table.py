"""add user table

Revision ID: 024c90b5ce2b
Revises: 13511b7b3540
Create Date: 2022-01-02 16:44:21.619373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '024c90b5ce2b'
down_revision = '13511b7b3540'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
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