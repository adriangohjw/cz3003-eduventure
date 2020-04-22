import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from services.quiz.operations.rs_quiz_course_assigns_operations import (
    initializeRsQuizCourseAssign,
    courseMngReadOperation,
    courseMngCreateOperation
)
from exceptions import ErrorWithCode

from models import (
    db, User,Staff,Quiz,Course, Rs_quiz_course_assign
)
from run_test import create_app
from services.core.operations.users_operations import encrypt

app = create_app()
app.app_context().push()
db.init_app(app)


"""
This is a TestCase object to test the functions in rs_quiz_course_assigns_operations.py
"""
class Test_rs_quiz_course_assigns_operations(unittest.TestCase):
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

        # adding courses
        course = Course(index='cz3003')
        db.session.add(course)

        # adding users
        user = User(
            email='staff@gmail.com',
            encrypted_password=encrypt('password'),
            name='staff'
        )
        staff = Staff(user)
        db.session.add(staff)

        # adding quizzes
        qz = Quiz(1, 'quiz', True, '2020-03-21', '2020-03-22')
        db.session.add(qz)

        # adding RsQuizCourseAssign
        rs = initializeRsQuizCourseAssign(1,'cz3003')
        db.session.add(rs)

        db.session.commit()

    # test the function courseMngCreateOperation
    def test_courseMngCreateOperation(self):

        # check that error raised when record (course) does not exist
        print('--- check that error raised when record (course) does not exist')
        with self.assertRaises(ErrorWithCode):
            courseMngCreateOperation(1,"cz3007")

        # check that error raised when record (quiz) does not exist
        print('--- check that error raised when record (quiz) does not exist')
        with self.assertRaises(ErrorWithCode):
            courseMngCreateOperation(2, "cz3007")

        # check that error raised when record already exist
        print('--- check that error raised when record already exist')
        with self.assertRaises(ErrorWithCode):
            courseMngCreateOperation(1, "cz3003")

        # adding courses
        course = Course(index='cz3007')
        db.session.add(course)
        db.session.commit()

        rs = courseMngCreateOperation(1,"cz3007")
        
        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(rs), Rs_quiz_course_assign)

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(rs.quiz_id, 1)
        self.assertEqual(rs.course_index, 'cz3007')

    # test the function courseMngReadOperation
    def test_courseMngReadOperation(self):

        # check that error raised when record does not exist
        print('--- check that error raised when record does not exist')
        with self.assertRaises(ErrorWithCode):
            courseMngReadOperation(2)

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(courseMngReadOperation(1)), Quiz)

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(courseMngReadOperation(1).name, 'quiz')

if __name__ == '__main__':
    unittest.main(verbosity=2)
