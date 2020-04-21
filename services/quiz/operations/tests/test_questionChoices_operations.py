import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from services.quiz.operations.questionChoices_operations import (
    initializeQuestionChoice,
    questionChoiceCreateOperation,
    questionChoiceDeleteOperation,
    questionChoiceReadOperation,
    questionChoiceUpdateOperation
)
from exceptions import ErrorWithCode

from models import (
    db, User, Student,Lesson,Question,Topic, QuestionChoice
)
from run_test import create_app
from services.core.operations.users_operations import encrypt

app = create_app()
app.app_context().push()
db.init_app(app)


"""
This is a TestCase object to test the functions in questionChoices_operations.py
"""
class Test_questionChoices_operations(unittest.TestCase):
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
        
        # add lessons
        lesson = Lesson(topic_id='1', id='3', name='se', content='test')
        db.session.add(lesson)

        # add questions
        qn = Question('1', '3', 'easy')
        db.session.add(qn)

        # add questionChoice
        qc = initializeQuestionChoice(1,'A',False)
        db.session.add(qc)

        db.session.commit()

    # test the function questionChoiceCreateOperation
    def test_questionChoiceCreateOperation(self):

        # check that error raised when record (question) does not exist
        print('--- check that error raised when record (question) does not exist')
        with self.assertRaises(ErrorWithCode):
            questionChoiceCreateOperation(2,"A",False)

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(questionChoiceCreateOperation(1,"B",False)), QuestionChoice)

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(questionChoiceCreateOperation(1,"B",False).description, 'B')

    # test the function questionChoiceReadOperation
    def test_questionChoiceReadOperation(self):

        # check that error raised when record does not exist
        print('--- check that error raised when record does not exist')
        with self.assertRaises(ErrorWithCode):
            questionChoiceReadOperation(1,3)

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(questionChoiceReadOperation(1,1)), QuestionChoice)

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(questionChoiceReadOperation(1,1).description, 'A')

    # test the function questionChoiceUpdateOperation
    def test_questionChoiceUpdateOperation(self):

        # check that error raised when record does not exist
        print('--- check that error raised when record does not exist')
        with self.assertRaises(ErrorWithCode):
            questionChoiceUpdateOperation(1,3,'description',None)

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(questionChoiceUpdateOperation(1,1,'description',None).description, 'description')

    # test the function questionChoiceDeleteOperation
    def test_questionChoiceDeleteOperation(self):

        # check that error raised when record does not exist
        print('--- check that error raised when record does not exist')
        with self.assertRaises(ErrorWithCode):
            questionChoiceDeleteOperation(1,3)

        # check that record has been deleted (number of record in database -1)
        print('--- check that record has been deleted (-1 number of record in database)')
        self.assertEqual(len(QuestionChoice.query.filter_by(question_id=1).filter_by(id=1).all()), 1)
        questionChoiceDeleteOperation(1,1)
        self.assertEqual(len(QuestionChoice.query.filter_by(question_id=1).filter_by(id=1).all()), 0)

if __name__ == '__main__':
    unittest.main(verbosity=2)
