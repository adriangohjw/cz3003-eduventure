import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest 

from models import db
from run_test import create_app

app = create_app()
app.app_context().push()
db.init_app(app)

from services.quiz.dao.QuizzesDAO import (
    quizCreate, 
    quizRead, 
    quizUpdate, 
    quizDelete
)
from models import (
    Quiz, User, Staff
)
from services.core.operations.users_operations import encrypt


"""
This is a TestCase object to test the functions in QuizzesDAO.py
"""
class Test_quizzes_dao(unittest.TestCase):
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
            email = 'john_doe@gmail.com',
            encrypted_password=encrypt('password'),
            name = 'john_doe'
        )
        staff = Staff(user)
        db.session.add(staff)

        db.session.commit()

    # test the function quizCreate
    def test_quizCreate(self):
        
        # create a new Quiz object
        quiz = Quiz(
            staff_id = 1,
            name = "Quiz Test",
            is_fast = True,
            date_start = '2020-03-01',
            date_end = '2020-03-31',
        )

        # add Quiz object to the database
        quizCreate(quiz)

        # retrieve all records from the table 'quizzes'
        quiz_list = Quiz.query.all()

        # check that the number of record added is correct
        print('--- check that the number of record added is correct')
        self.assertEqual(1, len(quiz_list))

        # check that the value(s) of the Quiz object added is correct
        print('--- check that the value(s) of the Quiz object added is correct')
        self.assertEqual(quiz_list[0].name, 'Quiz Test')

    # test the function quizRead
    def test_quizRead(self):
        
        # create a new Quiz object and add it to the database
        quiz = Quiz(
            staff_id = 1,
            name = "Quiz Test",
            is_fast = True,
            date_start = '2020-03-01',
            date_end = '2020-03-31',
        )
        db.session.add(quiz)
        db.session.commit()

        # check that the record retrieved is correct
        print('--- check that the record retrieved is correct')
        self.assertEqual(quizRead(1).name, 'Quiz Test')

    # test the function quizUpdate
    def test_quizUpdate(self):
        
        # create a new Quiz object and add it to the database
        quiz = Quiz(
            staff_id = 1,
            name = "Quiz Test",
            is_fast = True,
            date_start = '2020-03-01',
            date_end = '2020-03-31',
        )
        db.session.add(quiz)
        db.session.commit()

        # update value of Quiz object
        quiz.name = "Quiz Test 2"
        quizUpdate()

        # fetch updated User object from the database
        quiz = Quiz.query.filter_by(id=1).first()

        # check if value of Quiz has been updated
        print('--- check if value of Quiz object has been updated')
        self.assertEqual('Quiz Test 2', quiz.name)

    # test the function quizDelete
    def test_quizDelete(self):
        
        # create a new Quiz object and add it to the database
        quiz = Quiz(
            staff_id = 1,
            name = "Quiz Test",
            is_fast = True,
            date_start = '2020-03-01',
            date_end = '2020-03-31',
        )
        db.session.add(quiz)
        db.session.commit()

        # check that record has been deleted (number of record in database -1)
        print('--- check that record has been deleted (-1 number of record in database)')
        self.assertEqual(1, len(Quiz.query.all()))
        quizDelete(1)
        self.assertEqual(0, len(Quiz.query.all()))


if __name__ == '__main__':
    unittest.main(verbosity=2)
