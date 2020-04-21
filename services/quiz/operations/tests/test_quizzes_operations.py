import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest

from services.quiz.operations.quizzes_operations import (
    initializeQuiz,
    quizCreateOperation,
    quizDeleteOperation,
    quizReadOperation,
    quizUpdateOperation
)
from exceptions import ErrorWithCode

from models import (
    db, User,Staff,Quiz
)
from run_test import create_app
from services.core.operations.users_operations import encrypt

app = create_app()
app.app_context().push()
db.init_app(app)

import datetime


"""
This is a TestCase object to test the functions in quizzes_operations.py
"""
class Test_quizzes_operations(unittest.TestCase):
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

        # addingusers
        user = User(
            email='staff@gmail.com',
            encrypted_password=encrypt('password'),
            name='staff'
        )
        stf = Staff(user=user)
        db.session.add(stf)

        # adding quizzes
        q = initializeQuiz(1, "quiz1",True, "2020-03-20", "2020-03-21")
        db.session.add(q)

        db.session.commit()

    # test the function quizCreateOperation
    def test_quizCreateOperation(self):

        # check that error raised when record (staff) does not exist
        print('--- check that error raised when record (staff) does not exist')
        with self.assertRaises(ErrorWithCode):
            quizCreateOperation(2,"quiz2",False,"2020-02-22","2020-03-22")

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(quizCreateOperation(1, "quiz2", False, "2020-02-22", "2020-03-22")), Quiz)

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(quizCreateOperation(1, "quiz3", False, "2020-02-22", "2020-03-22").name, 'quiz3')

    # test the function quizReadOperation
    def test_quizReadOperation(self):

        # check that error raised when record does not exist
        print('--- check that error raised when record does not exist')
        with self.assertRaises(ErrorWithCode):
            quizReadOperation(2)

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(quizReadOperation(1)), Quiz)

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(quizReadOperation(1).name, 'quiz1')

    # test the function quizUpdateOperation
    def test_quizUpdateOperation(self):
        
        # check that error raised when record does not exist
        print('--- check that error raised when record does not exist')
        with self.assertRaises(ErrorWithCode):
            quizUpdateOperation(2, 'new_name', False, "2020-03-20", "2020-03-21")

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        quiz = quizUpdateOperation(1, 'new_name', False, None, None)
        self.assertEqual(quiz.name, 'new_name')
        self.assertEqual(quiz.is_fast, False)

    # test the function 
    def test_quizDeleteOperation(self):

        # check that error raised when record does not exist
        print('--- check that error raised when record does not exist')
        with self.assertRaises(ErrorWithCode):
            quizDeleteOperation(2)

        # check that record has been deleted (number of record in database -1)
        print('--- check that record has been deleted (-1 number of record in database)')
        self.assertEqual(len(Quiz.query.all()), 1)
        quizDeleteOperation(1)
        self.assertEqual(len(Quiz.query.all()), 0)

if __name__ == '__main__':
    unittest.main(verbosity=2)
