"""empty message

Revision ID: 72e0ead454ca
Revises: 
Create Date: 2018-11-30 10:52:35.263853

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72e0ead454ca'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('api_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.String(length=50), nullable=True),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('can_debit', sa.Boolean(), nullable=True),
    sa.Column('can_credit', sa.Boolean(), nullable=True),
    sa.Column('mml_username', sa.String(length=20), nullable=True),
    sa.Column('mml_password', sa.String(length=20), nullable=True),
    sa.Column('virtual_number', sa.String(length=20), nullable=True),
    sa.Column('user_type', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('mml_password'),
    sa.UniqueConstraint('mml_username'),
    sa.UniqueConstraint('public_id'),
    sa.UniqueConstraint('username'),
    sa.UniqueConstraint('virtual_number')
    )
    op.create_table('api_user_token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=256), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('user_public_id', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('api_user_token')
    op.drop_table('api_user')
    # ### end Alembic commands ###
