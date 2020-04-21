import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from models import (
    db, Question,Topic,Lesson,QuestionChoice
)
from run_test import create_app
from datetime import datetime

app = create_app()
app.app_context().push()
db.init_app(app)

from services.quiz.dao.QuestionChoicesDAO import (
    questionChoiceCreate,
    questionChoiceDelete,
    questionChoiceRead,
    questionChoiceUpdate,
    getLastQuestionChoiceID
)


"""
This is a TestCase object to test the functions in QuestionChoicesDAO.py
"""
class Test_QuestionChoicesDAO(unittest.TestCase):
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

        # adding lessons
        lesson = Lesson(topic_id='1', id='3', name='se', content='test')
        db.session.add(lesson)

        # adding questions
        qn = Question('1', '3', 'easy')
        db.session.add(qn)

        db.session.commit()

    # test the function questionChoiceCreate
    def test_questionChoiceCreate(self):

        # create a new QuestionChoice object
        qnCh = QuestionChoice(1,1,"A",False)

        # add QuestionChoice object to the database
        questionChoiceCreate(qnCh)

        # retrieve all records from the table 'questionchoices'
        qnCh_list = QuestionChoice.query.all()

        # check that the number of record added is correct
        print('--- check that the number of record added is correct')
        self.assertEqual(1, len(qnCh_list))

        # check that the value(s) of the QuestionChoice object added is correct
        print('--- check that the value(s) of the QuestionChoice object added is correct')
        self.assertEqual(qnCh_list[0].question_id, 1)

    # test the function questionChoiceRead
    def test_questionChoiceRead(self):

        # create a new QuestionChoice object and add it to the database
        qnCh = QuestionChoice(1, 1, "A", False)
        db.session.add(qnCh)
        db.session.commit()

        # check that the record retrieved is correct
        print('--- check that the record retrieved is correct')
        self.assertEqual(questionChoiceRead(1,1).description, 'A')

    # test the function questionChoiceUpdate
    def test_questionChoiceUpdate(self):

        # create a new QuestionChoice object and add it to the database
        qnCh = QuestionChoice(1, 1, "A", False)
        db.session.add(qnCh)
        db.session.commit()

        # update value of QuestionChoice object
        qnCh.is_correct = True
        questionChoiceUpdate()

        # fetch updated QuestionChoice object from the database
        qnCh = QuestionChoice.query.filter_by(question_id=1).filter_by(id=1).first()

        # check if value of QuestionChoice object has been updated
        print('--- check if value of QuestionChoice object has been updated')
        self.assertEqual(True, qnCh.is_correct)

    # test the function questionChoiceDelete
    def test_questionChoiceDelete(self):

        # create a new QuestionChoice object and add it to the database
        qnCh = QuestionChoice(1, 1, "A", False)
        db.session.add(qnCh)
        db.session.commit()

        # check that record has been deleted (number of record in database -1)
        print('--- check that record has been deleted (-1 number of record in database)')
        self.assertEqual(1, len(QuestionChoice.query.all()))
        questionChoiceDelete(1,1)
        self.assertEqual(0, len(QuestionChoice.query.all()))

    # test the function getLastQuestionChoiceID
    def test_getLastQuestionChoiceID(self):

        # check that function returns the right result (when number of record = 0)
        print('--- check that function returns the right result (when number of record = 0)')
        self.assertEqual(getLastQuestionChoiceID(1), 0)

        # create 2 QuestionChoice object and add them to the database
        # commit separately to ensure their commit order is correct
        qnCh = QuestionChoice(1, 4, "B", False)
        db.session.add(qnCh)
        db.session.commit()
        qnChLast = QuestionChoice(1, 2, "C", True)
        db.session.add(qnChLast)
        db.session.commit()

        # check that function returns the right result (when number of record = 2)
        print('--- check that function returns the right result (when number of record = 2)')
        self.assertEqual(getLastQuestionChoiceID(1), 2)

if __name__ == '__main__':
    unittest.main(verbosity=2)
