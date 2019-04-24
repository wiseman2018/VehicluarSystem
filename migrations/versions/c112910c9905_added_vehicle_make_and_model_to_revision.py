"""added vehicle make and model to revision

Revision ID: c112910c9905
Revises: 8fece3b346d4
Create Date: 2019-04-23 11:03:15.300944

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c112910c9905'
down_revision = '8fece3b346d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tenant_guests', sa.Column('vehicle_make', sa.String(length=128), nullable=True))
    op.add_column('tenant_guests', sa.Column('vehicle_model', sa.String(length=128), nullable=True))
    op.add_column('tenant_vehicles', sa.Column('vehicle_make', sa.String(length=128), nullable=True))
    op.add_column('tenant_vehicles', sa.Column('vehicle_model', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tenant_vehicles', 'vehicle_model')
    op.drop_column('tenant_vehicles', 'vehicle_make')
    op.drop_column('tenant_guests', 'vehicle_model')
    op.drop_column('tenant_guests', 'vehicle_make')
    # ### end Alembic commands ###