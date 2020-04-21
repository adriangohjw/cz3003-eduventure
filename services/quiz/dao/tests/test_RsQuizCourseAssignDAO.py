import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from models import (
    db, User, Staff, Course,Rs_quiz_course_assign, Quiz
)
from run_test import create_app
from services.core.operations.users_operations import encrypt
app = create_app()
app.app_context().push()
db.init_app(app)

from services.quiz.dao.RsQuizCourseAssignDAO import (
    rsQuizCourseAssignCreate,
    rsQuizCourseAssignRead
)


"""
This is a TestCase object to test the functions in RsQuizCourseAssignDAO.py
"""
class Test_RsQuizCourseAssignDAO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # this will run before every test
    # it will ensure that every test start with a fresh database
    def setUp(self):
        print('\r')
        # drop all tables in the database
        db.session.remove()
        db.drop_all()
        # crete all tables in the database
        db.create_all()

        # adding users
        user = User(
            email='john_doe@gmail.com',
            encrypted_password=encrypt('password'),
            name='john_doe'
        )
        staff = Staff(user)
        db.session.add(staff)

        # adding courses
        course = Course(index='cz3003')
        db.session.add(course)

        # adding quizzes
        quiz = Quiz(
            staff_id=1,
            name="Quiz Test",
            is_fast=True,
            date_start='2020-03-01',
            date_end='2020-03-31',
        )
        db.session.add(quiz)

        db.session.commit()

    # test the function rsQuizCourseAssignCreate
    def test_rsQuizCourseAssignCreate(self):
        
        # create a new relationship object
        rs = Rs_quiz_course_assign(1,'cz3003')

        # add relationship object to the database
        rsQuizCourseAssignCreate(rs)

        # retrieve all records from the table
        rs_list = Rs_quiz_course_assign.query.all()

        # check that the number of record added is correct
        print('--- check that the number of record added is correct')
        self.assertEqual(1, len(rs_list))

        # check that the value(s) of the relationship object added is correct
        print('--- check that the value(s) of the relationship object added is correct')
        self.assertEqual(rs_list[0].quiz_id, 1)

    # test the function rsQuizCourseAssignRead
    def test_rsQuizCourseAssignRead(self):

        # create a new relationship object and add it to the database
        rs = Rs_quiz_course_assign(1, 'cz3003')
        db.session.add(rs)
        db.session.commit()

        # check that the record retrieved is correct
        print('--- check that the record retrieved is correct')
        self.assertTrue(rsQuizCourseAssignRead(1,'cz3003'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
