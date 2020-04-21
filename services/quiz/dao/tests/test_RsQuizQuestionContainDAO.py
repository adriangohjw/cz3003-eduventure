import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest

from models import db
from run_test import create_app
app = create_app()
app.app_context().push()
db.init_app(app)

from models import (
    User, Staff, Course, Rs_quiz_question_contain, Quiz, Topic, Lesson, Question
)
from services.core.operations.users_operations import encrypt
from services.quiz.dao.RsQuizQuestionContainDAO import (
    rsQuizQuestionContainCreate,
    rsQuizQuestionContainRead,
    rsQuizQuestionContainDelete
)
    

"""
This is a TestCase object to test the functions in RsQuizQuestionContainDAO.py
"""
class Test_RsQuizQuestionContainDAO(unittest.TestCase):
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
            email='john_doe@gmail.com',
            encrypted_password=encrypt('password'),
            name='john_doe'
        )
        staff = Staff(user)
        db.session.add(staff)

        # adding courses
        course = Course(index='cz3003')
        db.session.add(course)

        # adding quizzes
        quiz = Quiz(
            staff_id=1,
            name="Quiz Test",
            is_fast=True,
            date_start='2020-03-01',
            date_end='2020-03-31',
        )
        db.session.add(quiz)

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

    # test the function rsQuizQuestionContainCreate
    def test_rsQuizQuestionContainCreate(self):

        # create a new relationship object
        rs = Rs_quiz_question_contain(1,1)

        # add relationship object to the database
        rsQuizQuestionContainCreate(rs)
        
        # retrieve all records from the table
        rs_list = Rs_quiz_question_contain.query.all()

        # check that the number of record added is correct
        print('--- check that the number of record added is correct')
        self.assertEqual(1, len(rs_list))

        # check that the value(s) of the relationship object added is correct
        print('--- check that the value(s) of the relationship object added is correct')
        self.assertEqual(rs_list[0].quiz_id, 1)

    # test the function rsQuizQuestionContainRead
    def test_rsQuizQuestionContainRead(self):

        # create a new relationship object and add it to the database
        rs = Rs_quiz_question_contain(1, 1)
        db.session.add(rs)
        db.session.commit()

        # check that the record retrieved is correct
        print('--- check that the record retrieved is correct')
        self.assertEqual(rsQuizQuestionContainRead(1,1).quiz_id, 1)
        self.assertEqual(rsQuizQuestionContainRead(1,1).question_id, 1)

    # test the function rsQuizQuestionContainDelete
    def test_rsQuizQuestionContainDelete(self):

        # create a new relationship object and add it to the database
        rs = Rs_quiz_question_contain(1, 1)
        db.session.add(rs)
        db.session.commit()

        # check that function returns the right result (when number of record = 1)
        print('--- check that function returns the right result (when number of record = 1)')
        self.assertIsNotNone(Rs_quiz_question_contain.query.filter_by(quiz_id=1).filter_by(question_id=1).first())
        rsQuizQuestionContainDelete(1, 1)
        self.assertIsNone(Rs_quiz_question_contain.query.filter_by(quiz_id=1).filter_by(question_id=1).first())
        

if __name__ == '__main__':
    unittest.main(verbosity=2)
