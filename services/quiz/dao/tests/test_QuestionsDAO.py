import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from models import (
    db, Question, Topic, Lesson
)
from run_test import create_app

app = create_app()
app.app_context().push()
db.init_app(app)

from services.quiz.dao.QuestionsDAO import (
    questionCreate, 
    questionDelete, 
    questionRead, 
    questionUpdate, 
    questionGetAllRead
)
    

"""
This is a TestCase object to test the functions in QuestionsDAO.py
"""
class Test_QuestionsDAO(unittest.TestCase):
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

        db.session.commit()

    # test the function questionCreate
    def test_questionCreate(self):

        # create a new Question object
        qn = Question('1', '3', 'easy')

        # add Question object to the database
        questionCreate(qn)

        # retrieve all records from the table 'questions'
        qn_list = Question.query.all()

        # check that the number of record added is correct
        print('--- check that the number of record added is correct')
        self.assertEqual(1, len(qn_list))

        # check that the value(s) of the Question object added is correct
        print('--- check that the value(s) of the Question object added is correct')
        self.assertEqual(qn_list[0].topic_id, 1)

    # test the function questionRead
    def test_questionRead(self):

        # create a new Question object and add it to the database
        qn = Question('1', '3', 'easy')
        db.session.add(qn)
        db.session.commit()

        # check that the record retrieved is correct
        print('--- check that the record retrieved is correct')
        self.assertEqual(questionRead(1).description, 'easy')

    # test the function questionUpdate
    def test_questionUpdate(self):

        # create a new Question object and add it to the database
        qn = Question('1', '3', 'easy')
        db.session.add(qn)
        db.session.commit()

        # update value of Question object
        qn.description = "Intermediate"
        questionUpdate()

        # fetch updated Question object from the database
        qn = Question.query.filter_by(topic_id=1).first()

        # check if value of Question object has been updated
        print('--- check if value of Question object has been updated')
        self.assertEqual('Intermediate', qn.description)

    # test the function questionDelete
    def test_questionDelete(self):

        # create a new Question object and add it to the database
        qn = Question('1', '3', 'easy')
        db.session.add(qn)
        db.session.commit()

        # check that record has been deleted (number of record in database -1)
        print('--- check that record has been deleted (-1 number of record in database)')
        self.assertEqual(1, len(Question.query.all()))
        questionDelete(1)
        self.assertEqual(0, len(Question.query.all()))

    # test the function questionGetAllRead
    def test_questionGetAllRead(self):

        # check that function returns the right result (when number of record = 0)
        print('--- check that function returns the right result (when number of record = 0)')
        self.assertEqual(len(questionGetAllRead()), 0)

        # create new Question objects and add it to the database
        qn1 = Question('1', '3', 'question_1')
        db.session.add(qn1)
        qn2 = Question('1', '3', 'question_2')
        db.session.add(qn2)
        qn3 = Question('1', '3', 'question_3')
        db.session.add(qn3)
        db.session.commit()

        # check that function returns the right result (when number of record = 3)
        print('--- check that function returns the right result (when number of record = 3)')
        self.assertEqual(len(questionGetAllRead()), 3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
