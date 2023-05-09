"""empty message

Revision ID: 460b998af377
Revises: a923aa5edd21
Create Date: 2023-05-08 05:34:42.416730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '460b998af377'
down_revision = 'a923aa5edd21'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.alter_column('population',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('climate',
               existing_type=sa.VARCHAR(length=30),
               nullable=True)
        batch_op.alter_column('terrain',
               existing_type=sa.VARCHAR(length=30),
               nullable=True)
        batch_op.alter_column('diameter',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('rotation_period',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('orbital_period',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('gravity',
               existing_type=sa.VARCHAR(length=30),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.alter_column('gravity',
               existing_type=sa.VARCHAR(length=30),
               nullable=False)
        batch_op.alter_column('orbital_period',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('rotation_period',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('diameter',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('terrain',
               existing_type=sa.VARCHAR(length=30),
               nullable=False)
        batch_op.alter_column('climate',
               existing_type=sa.VARCHAR(length=30),
               nullable=False)
        batch_op.alter_column('population',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
