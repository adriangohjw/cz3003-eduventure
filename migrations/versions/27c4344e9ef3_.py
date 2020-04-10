"""empty message

Revision ID: 27c4344e9ef3
Revises: a09d09245f41
Create Date: 2020-04-11 00:56:03.669531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27c4344e9ef3'
down_revision = 'a09d09245f41'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'rs_lesson_quiz_contains', ['topic_id', 'lesson_id', 'quiz_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'rs_lesson_quiz_contains', type_='unique')
    # ### end Alembic commands ###
