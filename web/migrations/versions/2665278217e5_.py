"""empty message

Revision ID: 2665278217e5
Revises: 
Create Date: 2021-01-02 23:12:07.034960

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2665278217e5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('remotes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('commands',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('remote_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('decodeType', sa.Integer(), nullable=True),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.Column('raw', sa.String(), nullable=True),
    sa.Column('rawLen', sa.Integer(), nullable=True),
    sa.Column('bitLen', sa.Integer(), nullable=True),
    sa.Column('position', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['remote_id'], ['remotes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('commands')
    op.drop_table('remotes')
    # ### end Alembic commands ###
