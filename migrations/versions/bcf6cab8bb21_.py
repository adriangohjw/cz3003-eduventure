"""empty message

Revision ID: bcf6cab8bb21
Revises: efa0491a74f4
Create Date: 2020-03-12 07:55:27.670329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bcf6cab8bb21'
down_revision = 'efa0491a74f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Rs_student_course_enrols',
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('course_index', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['course_index'], ['courses.index'], ),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('student_id', 'course_index')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Rs_student_course_enrols')
    # ### end Alembic commands ###
