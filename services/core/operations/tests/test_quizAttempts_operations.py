import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from services.core.operations.quizAttempts_operations import quizAttemptCreateOperation, quizAttemptListReadOperation,initializeQuizAttempt
from exceptions import ErrorWithCode

from models import db, User, Student,Staff,Quiz
from run_test import create_app
from services.core.operations.users_operations import encrypt

app = create_app()
app.app_context().push()
db.init_app(app)


class Test_quizAttempts_operations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()
        user = User(
            email='staff@gmail.com',
            encrypted_password=encrypt('password'),
            name='staff'
        )
        staff = Staff(user)
        db.session.add(staff)
        qz = Quiz(1, 'quiz', True, '2020-03-21', '2020-03-22')
        db.session.add(qz)
        qa = initializeQuizAttempt(2,1,100)
        db.session.add(qa)
        user = User(
            email='john_d@gmail.com',
            encrypted_password=encrypt('password'),
            name='john_doe'
        )
        # db.session.add(user)
        student = Student(user, 'U1722')
        db.session.add(student)
        db.session.commit()

    def test_quizAttemptCreateOperation(self):
        with self.assertRaises(ErrorWithCode):
            quizAttemptCreateOperation(3,1,20)
            quizAttemptCreateOperation(2,2,10)

            self.assertIsNotNone(quizAttemptCreateOperation(2,1,20))


    def test_quizAttemptListReadOperation(self):
        with self.assertRaises(ErrorWithCode):
            quizAttemptListReadOperation(1,2)
            quizAttemptListReadOperation(2,2)

        self.assertIsNotNone(quizAttemptListReadOperation(2,1))


if __name__ == '__main__':
    unittest.main()
