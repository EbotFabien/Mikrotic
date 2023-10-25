"""empty message

Revision ID: de3fa051a7d2
Revises: 47d98acfbe9e
Create Date: 2023-10-25 15:30:36.026344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de3fa051a7d2'
down_revision = '47d98acfbe9e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('router', schema=None) as batch_op:
        batch_op.add_column(sa.Column('version', sa.String(length=128), nullable=True))
        batch_op.add_column(sa.Column('model', sa.String(length=128), nullable=True))
        batch_op.add_column(sa.Column('firm_type', sa.String(length=128), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('router', schema=None) as batch_op:
        batch_op.drop_column('firm_type')
        batch_op.drop_column('model')
        batch_op.drop_column('version')

    # ### end Alembic commands ###