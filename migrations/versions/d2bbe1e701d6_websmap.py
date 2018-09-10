"""WebSMAP

Revision ID: d2bbe1e701d6
Revises: f892b3e50c75
Create Date: 2018-09-10 12:04:00.712888

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2bbe1e701d6'
down_revision = 'f892b3e50c75'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('websmap_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.String(length=50), nullable=True),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('can_debit', sa.Boolean(), nullable=True),
    sa.Column('can_credit', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('public_id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('websmap_user_token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=256), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('user_public_id', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('websmap_user_token')
    op.drop_table('websmap_user')
    # ### end Alembic commands ###
