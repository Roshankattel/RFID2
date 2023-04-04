"""Create posts table

Revision ID: 416d3ba22e6a
Revises: 
Create Date: 2023-04-04 17:58:00.816352

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '416d3ba22e6a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('user',sa.Column('id', sa.Integer(), nullable=False, primary_key=True))
    pass


def downgrade() -> None:
    op.drop_table("user")
    pass
