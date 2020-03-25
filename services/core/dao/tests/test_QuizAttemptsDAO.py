import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from models import db, QuizAttempt, Quiz, Staff, User,Topic,Lesson, Question,  Student
from run_test import create_app
from services.core.operations.users_operations import encrypt

app = create_app()
app.app_context().push()
db.init_app(app)

from services.core.dao.QuizAttemptsDAO import quizAttemptCreate,quizAttemptListRead


class Test_QuizAttemptsDAO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()
        user = User(
            email='john_d@gmail.com',
            encrypted_password=encrypt('password'),
            name='john_doe'
        )
        # db.session.add(user)
        student = Student(user, 'U1722')
        db.session.add(student)
        user = User(
            email='staff@gmail.com',
            encrypted_password=encrypt('password'),
            name='staff'
        )
        staff = Staff(user)
        db.session.add(staff)
        topic = Topic(name='seng')
        db.session.add(topic)
        lesson = Lesson(topic_id='1', id='3', name='se', content='test')
        db.session.add(lesson)
        qn = Question('1', '3', 'easy')
        db.session.add(qn)
        qz = Quiz(2,'quiz',True,'2020-03-21','2020-03-22') #staff id is 2 here, as it uses the fk of users table
        db.session.add(qz)
        db.session.commit()


    def test_quizAttemptCreate(self):
        qzAttempt = QuizAttempt(student_id=1, quiz_id=1, score=100)

        quizAttemptCreate(qzAttempt)

        qzAttempt_list = QuizAttempt.query.all()

        self.assertEqual(1, len(qzAttempt_list))
        self.assertEqual(qzAttempt_list[0].student_id, 1)

    def test_quizAttemptListRead(self):
        qzAttempt = QuizAttempt(student_id=1, quiz_id=1, score=100)
        db.session.add(qzAttempt)
        db.session.commit()
        self.assertEqual(1, len(quizAttemptListRead(student_id='1',quiz_id='1')))
        self.assertTrue(quizAttemptListRead(student_id='1',quiz_id='1'))


if __name__ == '__main__':
    unittest.main()
