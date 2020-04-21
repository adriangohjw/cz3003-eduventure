import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from services.core.operations.quizAttempts_operations import (
    quizAttemptCreateOperation, 
    quizAttemptListReadOperation,
    initializeQuizAttempt
)
from exceptions import ErrorWithCode

from models import (
    db, User, Student, Staff, Quiz, QuizAttempt
)
from run_test import create_app
from services.core.operations.users_operations import encrypt

app = create_app()
app.app_context().push()
db.init_app(app)


"""
This is a TestCase object to test the functions in quizAttempts_operations.py
"""
class Test_quizAttempts_operations(unittest.TestCase):
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
            email='staff@gmail.com',
            encrypted_password=encrypt('password'),
            name='staff'
        )
        staff = Staff(user)
        db.session.add(staff)

        user = User(
            email='john_d@gmail.com',
            encrypted_password=encrypt('password'),
            name='john_doe'
        )
        student = Student(user, 'U1722')
        db.session.add(student)

        # adding quizzes
        qz = Quiz(1, 'quiz', True, '2020-03-21', '2020-03-22')
        db.session.add(qz)

        # adding quizattempts
        qa = initializeQuizAttempt(2,1,100)
        db.session.add(qa)
        
        db.session.commit()

    # test the function quizAttemptCreateOperation
    def test_quizAttemptCreateOperation(self):

        # check that error raised when record (student) does not exist
        print('--- check that error raised when record (student) does not exist')
        with self.assertRaises(ErrorWithCode):
            quizAttemptCreateOperation(3,1,20)

        # check that error raised when record (quiz) does not exist
        print('--- check that error raised when record (quiz) does not exist')
        with self.assertRaises(ErrorWithCode):
            quizAttemptCreateOperation(2,2,10)

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(quizAttemptCreateOperation(2,1,20)), QuizAttempt)

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(quizAttemptCreateOperation(2,1,20).id, 3)

    # test the function quizAttemptListReadOperation
    def test_quizAttemptListReadOperation(self):

        # check that error raised when record (student) does not exist
        print('--- check that error raised when record (student) does not exist')
        with self.assertRaises(ErrorWithCode):
            quizAttemptListReadOperation(3,1)

        # check that error raised when record (quiz) does not exist
        print('--- check that error raised when record (quiz) does not exist')
        with self.assertRaises(ErrorWithCode):
            quizAttemptListReadOperation(2,2)

        # check that when successful, number of records returned by function is correct
        print('--- check that when successful, number of records returned by function is correct')
        self.assertEqual(len(quizAttemptListReadOperation(2,1)), 1)

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertIsNotNone(quizAttemptListReadOperation(2,1)[0].quiz_id, 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
