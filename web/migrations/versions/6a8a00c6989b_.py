"""empty message

Revision ID: 6a8a00c6989b
Revises: 2665278217e5
Create Date: 2021-01-15 20:24:27.638894

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a8a00c6989b'
down_revision = '2665278217e5'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('commands', 'value', existing_type=sa.Integer(), type_=sa.BigInteger())


def downgrade():
    op.alter_column('commands', 'value', existing_type=sa.BigInteger(), type_=sa.Integer())
