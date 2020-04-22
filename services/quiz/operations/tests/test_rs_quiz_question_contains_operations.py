import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest

from exceptions import ErrorWithCode

from models import db
from run_test import create_app
app = create_app()
app.app_context().push()
db.init_app(app)

from models import (
    User, Staff, Quiz, Course, Topic, Lesson, Question, Rs_quiz_question_contain
)
from services.core.operations.users_operations import encrypt
from services.quiz.operations.rs_quiz_question_contains_operations import (
    initializeRsQuizQuestionContain, 
    questionMngCreateOperation, 
    questionMngReadOperation, 
    questionMngDeleteOperation
)


"""
This is a TestCase object to test the functions in rs_quiz_question_contains_operations.py
"""
class Test_rs_quiz_question_contains_operations(unittest.TestCase):
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

        # adding topics
        topic = Topic(name='seng')
        db.session.add(topic)

        # adding lessons
        lesson = Lesson(topic_id=1, id=1, name='se', content='test')
        db.session.add(lesson)

        # adding questions
        qn = Question(1, 1, 'easy')
        db.session.add(qn)

        # adding RsQuizQuestionContain
        rs = initializeRsQuizQuestionContain(1,1)
        db.session.add(rs)

        db.session.commit()

    # test the function questionMngCreateOperation
    def test_questionMngCreateOperation(self):

        # check that error raised when record (question) does not exist
        print('--- check that error raised when record (question) does not exist')
        with self.assertRaises(ErrorWithCode):
            questionMngCreateOperation(1, 2)

        # check that error raised when record (quiz) does not exist
        print('--- check that error raised when record (quiz) does not exist')
        with self.assertRaises(ErrorWithCode):
            questionMngCreateOperation(2, 1)

        # check that error raised when record already exist
        print('--- check that error raised when record already exist')
        with self.assertRaises(ErrorWithCode):
            questionMngCreateOperation(1, 1)

        # adding questions
        qn = Question(1, 1, 'middle')
        db.session.add(qn)
        db.session.commit()

        rs = questionMngCreateOperation(1, 2)

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(rs), Rs_quiz_question_contain)

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(rs.quiz_id, 1)
        self.assertEqual(rs.question_id, 2)

    # test the function questionMngReadOperation
    def test_questionMngReadOperation(self):

        # check that error raised when record (quiz) does not exist
        print('--- check that error raised when record (quiz) does not exist')
        with self.assertRaises(ErrorWithCode):
            questionMngReadOperation(2)

        quiz = questionMngReadOperation(1)

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(quiz), Quiz)

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(quiz.name, 'quiz')

    # test the function questionMngDeleteOperation
    def test_questionMngDeleteOperation(self):

        # check that error raised when record does not exist
        print('--- check that error raised when record does not exist')
        with self.assertRaises(ErrorWithCode):
            questionMngDeleteOperation(2, 2)

        # check that record has been deleted (number of record in database -1)
        print('--- check that record has been deleted (-1 number of record in database)')
        self.assertEqual(len(Rs_quiz_question_contain.query.all()), 1)
        questionMngDeleteOperation(1, 1)
        self.assertEqual(len(Rs_quiz_question_contain.query.all()), 0)
    

if __name__ == '__main__':
    unittest.main(verbosity=2)
