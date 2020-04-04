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
        db.session.commit()
        q = initializeQuiz(1,"quiz1",True,"2020-03-20", "2020-03-21")
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
        name_original =q.name
        fast_original = q.is_fast

        quizUpdateOperation(1,"name","quiz3")
        quizUpdateOperation(1, "is_fast", False)

        q = Quiz.query.filter_by(id=1).first()
        self.assertNotEqual(name_original, q.name)
        self.assertNotEqual(fast_original, q.is_fast)

    def test_quizDeleteOperation(self):
        quizDeleteOperation(1)

        q = Quiz.query.filter_by(id=1).first()
        self.assertIsNone(q)

if __name__ == '__main__':
    unittest.main()
