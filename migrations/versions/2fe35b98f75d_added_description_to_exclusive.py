"""added description to exclusive

Revision ID: 2fe35b98f75d
Revises: 3199f253564d
Create Date: 2019-05-15 14:24:26.618052

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2fe35b98f75d'
down_revision = '3199f253564d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exclusive_list', sa.Column('description', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('exclusive_list', 'description')
    # ### end Alembic commands ###