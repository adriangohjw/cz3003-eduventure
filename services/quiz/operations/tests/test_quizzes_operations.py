import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest

from services.quiz.operations.quizzes_operations import initializeQuiz,quizCreateOperation,quizDeleteOperation,quizReadOperation,quizUpdateOperation
from exceptions import ErrorWithCode

from models import db, User,Staff,Quiz
from run_test import create_app
from services.core.operations.users_operations import encrypt

app = create_app()
app.app_context().push()
db.init_app(app)

import datetime


class Test_quizzes_operations(unittest.TestCase):
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
        stf = Staff(user=user)
        db.session.add(stf)

        q = initializeQuiz(1, "quiz1",True, "2020-03-20", "2020-03-21")
        db.session.add(q)

        db.session.commit()

    def test_quizCreateOperation(self):
        with self.assertRaises(ErrorWithCode):
            quizCreateOperation(2,"quiz2",False,"2020-02-22","2020-03-22")
            quizCreateOperation(1, "quiz2", False, "2020-2-22", "2020-3-22")
            quizCreateOperation(1, "quiz2", "invalid", "2020-2-22", "2020-3-22")

        self.assertIsNotNone(quizCreateOperation(1, "quiz2", False, "2020-02-22", "2020-03-22"))

    def test_quizReadOperation(self):
        with self.assertRaises(ErrorWithCode):
            quizReadOperation(2)

        self.assertIsNotNone( quizReadOperation(1))

    def test_quizUpdateOperation(self):
        q = Quiz.query.filter_by(id=1).first()
        date_start_original = q.date_start

        quizUpdateOperation(1, None, None, datetime.date(2020, 3, 10), None)
        q = Quiz.query.filter_by(id=1).first()
        self.assertEqual(datetime.date(2020, 3, 10), q.date_start)

        quizUpdateOperation(1, 'new_name', False, None, None)
        q = Quiz.query.filter_by(id=1).first()
        self.assertEqual('new_name', q.name)
        self.assertEqual(False, q.is_fast)

        self.assertRaises(ErrorWithCode, quizUpdateOperation, 1, None, None, datetime.date(2020, 3, 10), datetime.date(2020, 3, 9))


    def test_quizDeleteOperation(self):
        quizDeleteOperation(1)

        q = Quiz.query.filter_by(id=1).first()
        self.assertIsNone(q)

if __name__ == '__main__':
    unittest.main()
