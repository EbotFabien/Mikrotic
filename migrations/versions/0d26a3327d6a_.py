"""empty message

Revision ID: 0d26a3327d6a
Revises: 8be553807be1
Create Date: 2023-10-19 19:08:18.049167

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d26a3327d6a'
down_revision = '8be553807be1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('router', schema=None) as batch_op:
        batch_op.add_column(sa.Column('login', sa.String(length=128), nullable=True))
        batch_op.drop_column('user')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('router', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user', sa.VARCHAR(length=128), nullable=True))
        batch_op.drop_column('login')

    # ### end Alembic commands ###
