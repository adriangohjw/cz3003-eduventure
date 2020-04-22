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
    QuestionAttempt, Student, User,Question,Topic,Lesson
)
from services.core.operations.users_operations import encrypt
from services.core.dao.QuestionAttemptsDAO import (
    questionAttemptCreate,
    questionAttemptListRead
)


"""
This is a TestCase object to test the functions in QuestionAttemptsDAO.py
"""
class Test_QuestionAttemptsDAO(unittest.TestCase):
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
        lesson = Lesson(topic_id=1, id=1, name='se', content='test')
        db.session.add(lesson)

        # adding questions
        qn_1 = Question(1, 1,'easy')
        db.session.add(qn_1)

        qn_2 = Question(1, 1,'medium')
        db.session.add(qn_2)
        
        db.session.commit()

    # test the function questionAttemptCreate
    def test_questionAttemptCreate(self):

        # create a new QuestionAttempt object
        qnAttempt = QuestionAttempt(student_id=1, question_id=1, is_correct=True, duration_ms=20)
        
        # add QuizAttempt object to the database
        questionAttemptCreate(qnAttempt)

        # retrieve all records from the table 'questionattempts'
        qnAttempt_list = QuestionAttempt.query.all()

        # check that the number of record added is correct
        print('--- check that the number of record added is correct')
        self.assertEqual(1, len(qnAttempt_list))

        # check that the value(s) of the QuestionAttempt object added is correct
        print('--- check that the value(s) of the QuestionAttempt object added is correct')
        self.assertEqual(qnAttempt_list[0].student_id, 1)

    # test the function questionAttemptListRead
    def test_questionAttemptListRead(self):

        # check that the number of record retrieved is correct (number of record = 0)
        print('--- check that the number of record retrieved is correct (number of record = 0)')
        self.assertEqual(len(questionAttemptListRead(student_id=1, question_id=1)), 0)

        # create new QuestionAttempt objects and add it to the database
        qnAttempt_1 = QuestionAttempt(student_id=1, question_id=1, is_correct=True, duration_ms=20)
        db.session.add(qnAttempt_1)
        qnAttempt_2 = QuestionAttempt(student_id=1, question_id=2, is_correct=True, duration_ms=20)
        db.session.add(qnAttempt_2)
        db.session.commit()

        # check that the number of record retrieved is correct (number of record = 1)
        print('--- check that the number of record retrieved is correct (number of record = 1)')
        self.assertEqual(len(questionAttemptListRead(student_id=1, question_id=1)), 1)

        # check that the number of record retrieved is correct (number of record = 2)
        print('--- check that the number of record retrieved is correct (number of record = 2)')
        self.assertEqual(len(questionAttemptListRead(student_id=1)), 2)

        # check that the record retrieved is correct
        print('--- check that the record retrieved is correct')
        self.assertEqual(questionAttemptListRead(student_id=1, question_id=1)[0].duration_ms, 20)


if __name__ == '__main__':
    unittest.main(verbosity=2)
