import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from models import db, User, Staff, Course,Rs_quiz_course_assign, Quiz
from run_test import create_app
from services.core.operations.users_operations import encrypt
app = create_app()
app.app_context().push()
db.init_app(app)

from services.quiz.dao.RsQuizCourseAssignDAO import rsQuizCourseAssignCreate,rsQuizCourseAssignRead


class Test_RsQuizCourseAssignDAO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()
        user = User(
            email='john_doe@gmail.com',
            encrypted_password=encrypt('password'),
            name='john_doe'
        )
        staff = Staff(user)
        db.session.add(staff)
        course = Course(index='cz3003')
        db.session.add(course)
        quiz = Quiz(
            staff_id=1,
            name="Quiz Test",
            is_fast=True,
            date_start='2020-03-01',
            date_end='2020-03-31',
        )
        db.session.add(quiz)
        db.session.commit()

    def test_rsQuizCourseAssignCreate(self):
        rs = Rs_quiz_course_assign(1,'cz3003')
        rsQuizCourseAssignCreate(rs)
        rs_list = Rs_quiz_course_assign.query.all()

        self.assertEqual(1, len(rs_list))
        self.assertEqual(rs_list[0].quiz_id, 1)

    def test_rsQuizCourseAssignRead(self):
        rs = Rs_quiz_course_assign(1, 'cz3003')

        db.session.add(rs)
        db.session.commit()
        self.assertTrue(rsQuizCourseAssignRead(1,'cz3003'))


if __name__ == '__main__':
    unittest.main()
