import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from services.core.operations.questionAttempts_operations import (
    questionAttemptCreateOperation, 
    questionAttemptListReadOperation,
    initializeQuestionAttempt
)

from exceptions import ErrorWithCode

from models import (
    db, User, Student,Lesson,Question,Topic, QuestionAttempt 
)
from services.core.operations.users_operations import encrypt

from run_test import create_app

app = create_app()
app.app_context().push()
db.init_app(app)


"""
This is a TestCase object to test the functions in questionAttempts_operations.py
"""
class Test_questionAttempts_operations(unittest.TestCase):
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
            email='john_d@gmail.com',
            encrypted_password=encrypt('password'),
            name='john_doe'
        )
        student = Student(user, 'U1722')
        db.session.add(student)

        # adding topics
        topic = Topic(name='seng')
        db.session.add(topic)

        # adding lessons
        lesson = Lesson(topic_id='1', id='3', name='se', content='test')
        db.session.add(lesson)

        # adding questions
        qn = Question('1', '3', 'easy')
        db.session.add(qn)

        # adding queestionAttempts
        qa = initializeQuestionAttempt(1,1,True,30)
        db.session.add(qa)

        db.session.commit()

    # test the function questionAttemptCreateOperation
    def test_questionAttemptCreateOperation(self):

        # check that error raised when record (student) does not exist
        print('--- check that error raised when record (student) does not exist')
        with self.assertRaises(ErrorWithCode):
            questionAttemptCreateOperation(2,1,True,20)

        # check that error raised when record (question) does not exist
        print('--- check that error raised when record (question) does not exist')
        with self.assertRaises(ErrorWithCode):
            questionAttemptCreateOperation(1,2,False,10)

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(questionAttemptCreateOperation(1,1,True,15)), QuestionAttempt)

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(questionAttemptCreateOperation(1,1,True,15).id, 3)

    # test the function questionAttemptListReadOperation
    def test_questionAttemptListReadOperation(self):

        # check that error raised when record (student) does not exist
        print('--- check that error raised when record (student) does not exist')
        with self.assertRaises(ErrorWithCode):
            questionAttemptListReadOperation(2,1)

        # check that error raised when record (question) does not exist
        print('--- check that error raised when record (question) does not exist')
        with self.assertRaises(ErrorWithCode):
            questionAttemptListReadOperation(1,2)

        # check that when successful, number of records returned by function is correct
        print('--- check that when successful, number of records returned by function is correct')
        self.assertEqual(len(questionAttemptListReadOperation(1,1)), 1)

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(questionAttemptListReadOperation(1,1)[0].question_id, 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
