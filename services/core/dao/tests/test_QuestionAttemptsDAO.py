import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest

from models import db
from run_test import create_app
app = create_app()
app.app_context().push()
db.init_app(app)

from models import QuestionAttempt, Student, User,Question,Topic,Lesson
from services.core.operations.users_operations import encrypt
from services.core.dao.QuestionAttemptsDAO import questionAttemptCreate,questionAttemptListRead


class Test_QuestionAttemptsDAO(unittest.TestCase):

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
        student = Student(user, 'U1722')
        db.session.add(student)

        topic = Topic(name='seng')
        db.session.add(topic)

        lesson = Lesson(topic_id=1, id=1, name='se', content='test')
        db.session.add(lesson)

        qn = Question(1, 1,'easy')
        db.session.add(qn)
        db.session.commit()


    def test_questionAttemptCreate(self):

        self.assertEqual(len(QuestionAttempt.query.all()), 0)

        qnAttempt = QuestionAttempt(student_id=1, question_id=1, is_correct=True, duration_ms=20)
        questionAttemptCreate(qnAttempt)

        qnAttempt_list = QuestionAttempt.query.all()
        self.assertEqual(1, len(qnAttempt_list))
        self.assertEqual(qnAttempt_list[0].student_id, 1)


    def test_questionAttemptListRead(self):

        self.assertEqual(len(questionAttemptListRead(student_id=1, question_id=1)), 0)

        qnAttempt = QuestionAttempt(student_id=1, question_id=1, is_correct=True, duration_ms=20)
        db.session.add(qnAttempt)
        db.session.commit()

        self.assertEqual(questionAttemptListRead(student_id=1, question_id=1)[0].duration_ms, 20)


if __name__ == '__main__':
    unittest.main()
