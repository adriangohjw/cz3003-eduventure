"""empty message

Revision ID: 418545a9b711
Revises: 93386e6e3397
Create Date: 2020-04-10 16:48:06.686890

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '418545a9b711'
down_revision = '93386e6e3397'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('challenges', sa.Column('is_completed', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('challenges', 'is_completed')
    # ### end Alembic commands ###