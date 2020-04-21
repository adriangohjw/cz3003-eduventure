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
    QuizAttempt, Quiz, Staff, User,Topic,Lesson, Question, Student
)
from services.core.operations.users_operations import encrypt
from services.core.dao.QuizAttemptsDAO import (
    quizAttemptCreate,
    quizAttemptListRead
)


"""
This is a TestCase object to test the functions in QuizAttemptsDAO.py
"""
class Test_QuizAttemptsDAO(unittest.TestCase):
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

        user = User(
            email='staff@gmail.com',
            encrypted_password=encrypt('password'),
            name='staff'
        )
        staff = Staff(user)
        db.session.add(staff)

        # adding topics
        topic = Topic(name='seng')
        db.session.add(topic)

        # adding lessons
        lesson = Lesson(topic_id='1', id='3', name='se', content='test')
        db.session.add(lesson)

        # adding questions
        qn = Question('1', '3', 'easy')
        db.session.add(qn)

        # adding quizzes
        qz = Quiz(2, 'quiz', True, '2020-03-21', '2020-03-22')
        db.session.add(qz)

        db.session.commit()

    # test the function quizAttemptCreate
    def test_quizAttemptCreate(self):

        # create a new QuizAttempt object
        qzAttempt = QuizAttempt(student_id=1, quiz_id=1, score=100)

        # add QuizAttempt object to the database
        quizAttemptCreate(qzAttempt)

        # retrieve all records from the table 'quizattempts'
        qzAttempt_list = QuizAttempt.query.all()

        # check that the number of record added is correct
        print('--- check that the number of record added is correct')
        self.assertEqual(1, len(qzAttempt_list))

        # check that the value(s) of the QuizAttempt object added is correct
        print('--- check that the value(s) of the QuizAttempt object added is correct')
        self.assertEqual(qzAttempt_list[0].student_id, 1)

    # test the function quizAttemptListRead
    def test_quizAttemptListRead(self):

        # create a new QuizAttempt object and add it to the database
        qzAttempt = QuizAttempt(student_id=1, quiz_id=1, score=100)
        db.session.add(qzAttempt)
        db.session.commit()

        # check that the number of record retrieved is correct
        print('--- check that the number of record retrieved is correct')
        self.assertEqual(1, len(quizAttemptListRead(student_id='1',quiz_id='1')))

        # check that the record retrieved is correct
        print('--- check that the record retrieved is correct')
        self.assertEqual(quizAttemptListRead(student_id='1',quiz_id='1')[0].quiz_id, 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
