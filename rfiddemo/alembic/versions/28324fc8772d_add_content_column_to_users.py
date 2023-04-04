"""add content column to users

Revision ID: 28324fc8772d
Revises: 416d3ba22e6a
Create Date: 2023-04-04 18:07:56.330948

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28324fc8772d'
down_revision = '416d3ba22e6a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')  
    pass
