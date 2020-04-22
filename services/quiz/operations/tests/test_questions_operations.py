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
    User, Student,Lesson,Question,Topic, QuestionChoice
)
from services.core.operations.users_operations import encrypt
from services.quiz.operations.questions_operations import (
    questionCreateOperation, 
    questionDeleteOperation, 
    questionReadOperation, 
    questionUpdateOperation, 
    questionGetAllReadOperation
)


"""
This is a TestCase object to test the functions in questions_operations.py
"""
class Test_questions_operations(unittest.TestCase):
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

        # adding topics
        topic = Topic(name='seng')
        db.session.add(topic)

        # addinglessons
        lesson = Lesson(topic_id=1, id=1, name='se', content='test')
        db.session.add(lesson)

        # adding questions
        qn = Question(1, 1, 'easy')
        db.session.add(qn)

        db.session.commit()

    # test the function questionCreateOperation
    def test_questionCreateOperation(self):

        # check that error raised when record (topic) does not exist
        print('--- check that error raised when record (topic) does not exist')
        with self.assertRaises(ErrorWithCode):
            questionCreateOperation(1,2,"easy")

        # check that error raised when record (lesson) does not exist
        print('--- check that error raised when record (lesson) does not exist')
        with self.assertRaises(ErrorWithCode):
            questionCreateOperation(2,1, "easy")

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(questionCreateOperation(1,1, "intermediate")), Question)

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(questionCreateOperation(1,1, "intermediate").id, 3)

    # test the function questionReadOperation
    def test_questionReadOperation(self):

        # check that error raised when record does not exist
        print('--- check that error raised when record does not exist')
        with self.assertRaises(ErrorWithCode):
            questionReadOperation(2)

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(questionReadOperation(1)), Question)

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(questionReadOperation(1).description, 'easy')

    # test the function questionUpdateOperation
    def test_questionUpdateOperation(self):

        # check that error raised when record does not exist
        print('--- check that error raised when record does not exist')
        with self.assertRaises(ErrorWithCode):
            questionUpdateOperation(2, 'new_description')

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(questionUpdateOperation(1,"new_description").description, 'new_description')
        
    # test the function questionDeleteOperation
    def test_questionDeleteOperation(self):

        # check that error raised when record does not exist
        print('--- check that error raised when record does not exist')
        with self.assertRaises(ErrorWithCode):
            questionDeleteOperation(2)

        # check that record has been deleted (number of record in database -1)
        print('--- check that record has been deleted (-1 number of record in database)')
        self.assertEqual(len(Question.query.all()), 1)
        questionDeleteOperation(1)
        self.assertEqual(len(Question.query.all()), 0)

    # test the function questionGetAllReadOperation
    def test_questionGetAllReadOperation(self):
        
        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(1, len(questionGetAllReadOperation()))
        

if __name__ == '__main__':
    unittest.main(verbosity=2)
