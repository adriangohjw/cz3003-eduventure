"""empty message

Revision ID: cbd043af5fab
Revises: 5f2c7b15bef1
Create Date: 2020-04-10 00:28:49.274395

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cbd043af5fab'
down_revision = '5f2c7b15bef1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lessons', sa.Column('url_link', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('lessons', 'url_link')
    # ### end Alembic commands ###