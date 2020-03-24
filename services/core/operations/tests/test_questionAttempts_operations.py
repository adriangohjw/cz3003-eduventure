import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from services.core.operations.questionAttempts_operations import questionAttemptCreateOperation, questionAttemptListReadOperation,initializeQuestionAttempt

from exceptions import ErrorWithCode

from models import db, User, Student,Lesson,Question,Topic
from run_test import create_app
from services.core.operations.users_operations import encrypt

app = create_app()
app.app_context().push()
db.init_app(app)


class Test_questionAttempts_operations(unittest.TestCase):
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
        topic = Topic(name='seng')
        db.session.add(topic)
        lesson = Lesson(topic_id='1', id='3', name='se', content='test')
        db.session.add(lesson)
        qn = Question('1', '3', 'easy')
        db.session.add(qn)
        qa = initializeQuestionAttempt(1,1,True,30)
        db.session.add(qa)
        db.session.commit()

    def test_questionAttemptCreateOperation(self):
        with self.assertRaises(ErrorWithCode):
            questionAttemptCreateOperation(2,1,True,20)
            questionAttemptCreateOperation(1,2,False,10)

            self.assertIsNotNone(questionAttemptCreateOperation(1,1,True,15))
            qn = Question('1', '2', 'hard')
            db.session.add(qn)
            db.session.commit()
            self.assertIsNotNone(questionAttemptCreateOperation(1, 2, False, 15))
            self.assertIsNotNone(questionAttemptCreateOperation(1, 2, True, 15))

    def test_questionAttemptListReadOperation(self):
        with self.assertRaises(ErrorWithCode):
            questionAttemptListReadOperation(1,2)
            questionAttemptListReadOperation(2,1)

        self.assertIsNotNone(questionAttemptListReadOperation(1,1))


if __name__ == '__main__':
    unittest.main()
