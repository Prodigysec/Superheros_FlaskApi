"""Add stregnth attribute to HeroPower

Revision ID: dbd9e28f11fe
Revises: 999267d72fe2
Create Date: 2023-10-02 22:01:23.635545

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbd9e28f11fe'
down_revision = '999267d72fe2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('hero_powers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('strength', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('hero_powers', schema=None) as batch_op:
        batch_op.drop_column('strength')

    # ### end Alembic commands ###
