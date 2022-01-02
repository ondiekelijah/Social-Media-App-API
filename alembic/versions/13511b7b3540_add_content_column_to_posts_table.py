"""add content column to posts table

Revision ID: 13511b7b3540
Revises: b0e41ec36c43
Create Date: 2022-01-02 16:38:45.734611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13511b7b3540'
down_revision = 'b0e41ec36c43'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts' ,sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
