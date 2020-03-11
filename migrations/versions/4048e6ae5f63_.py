"""empty message

Revision ID: 4048e6ae5f63
Revises: 409f5e982c72
Create Date: 2020-03-12 07:24:25.709819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4048e6ae5f63'
down_revision = '409f5e982c72'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('questionchoices',
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('is_correct', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
    sa.PrimaryKeyConstraint('question_id', 'id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('questionchoices')
    # ### end Alembic commands ###
