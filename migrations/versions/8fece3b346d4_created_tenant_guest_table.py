"""created tenant guest table

Revision ID: 8fece3b346d4
Revises: d2ec263c8e7e
Create Date: 2019-04-16 10:50:24.690069

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fece3b346d4'
down_revision = 'd2ec263c8e7e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tenant_guests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tenant_id', sa.Integer(), nullable=True),
    sa.Column('tenant_name', sa.String(length=128), nullable=True),
    sa.Column('plate_number', sa.String(length=128), nullable=True),
    sa.Column('time_from', sa.DateTime(), nullable=True),
    sa.Column('time_to', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tenant_guests')
    # ### end Alembic commands ###
