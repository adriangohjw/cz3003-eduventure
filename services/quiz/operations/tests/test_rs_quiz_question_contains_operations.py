import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from services.quiz.operations.rs_quiz_question_contains_operations import initializeRsQuizQuestionContain,questionMngCreateOperation,questionMngReadOperation
from exceptions import ErrorWithCode

from models import db, User,Staff,Quiz,Course,Topic,Lesson,Question
from run_test import create_app
from services.core.operations.users_operations import encrypt

app = create_app()
app.app_context().push()
db.init_app(app)


class Test_rs_quiz_question_contains_operations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()
        course = Course(index='cz3003')
        db.session.add(course)
        db.session.commit()
        user = User(
            email='staff@gmail.com',
            encrypted_password=encrypt('password'),
            name='staff'
        )
        staff = Staff(user)
        db.session.add(staff)
        qz = Quiz(1, 'quiz', True, '2020-03-21', '2020-03-22')
        db.session.add(qz)
        topic = Topic(name='seng')
        db.session.add(topic)
        lesson = Lesson(topic_id='1', id='3', name='se', content='test')
        db.session.add(lesson)
        qn = Question('1', '3', 'easy')
        db.session.add(qn)
        rs = initializeRsQuizQuestionContain(1,1)
        db.session.add(rs)
        db.session.commit()

    def test_questionMngCreateOperation(self):
        with self.assertRaises(ErrorWithCode):
            questionMngCreateOperation(1,2)
            questionMngCreateOperation(2, 1)
            questionMngCreateOperation(1, 1)

        user = User(
            email='sjow@gmail.com',
            encrypted_password=encrypt('password'),
            name='jow'
        )
        staff = Staff(user)
        db.session.add(staff)
        qz = Quiz(2, 'quiz', True, '2020-03-21', '2020-03-22')
        db.session.add(qz)
        topic = Topic(name='srs')
        db.session.add(topic)
        lesson = Lesson(topic_id='2', id='2', name='srs1', content='intro')
        db.session.add(lesson)
        qn = Question('2', '2', 'easy')
        db.session.add(qn)
        self.assertIsNotNone(questionMngCreateOperation(2, 1))#2 quizes have the same questions
        self.assertIsNotNone(questionMngCreateOperation(1,2))#one quiz to diff questions

    def test_questionMngReadOperation(self):
        with self.assertRaises(ErrorWithCode):
            questionMngReadOperation(2)

        self.assertIsNotNone( questionMngReadOperation(1))

if __name__ == '__main__':
    unittest.main()
