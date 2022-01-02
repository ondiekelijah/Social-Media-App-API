"""create posts table

Revision ID: b0e41ec36c43
Revises: 
Create Date: 2022-01-02 16:29:14.769452

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0e41ec36c43'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('title', sa.String(), nullable=False),
    )


def downgrade():
    op.drop_table('posts')
