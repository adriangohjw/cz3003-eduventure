"""empty message

Revision ID: 31930450b94b
Revises: dff1a0a50b0c
Create Date: 2020-03-12 07:39:56.990944

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31930450b94b'
down_revision = 'dff1a0a50b0c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('questionattempts',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('is_correct', sa.Boolean(), nullable=False),
    sa.Column('duration', sa.Interval(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'question_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('questionattempts')
    # ### end Alembic commands ###
