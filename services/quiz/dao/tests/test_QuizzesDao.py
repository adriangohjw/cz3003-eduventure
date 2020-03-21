import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest 

from models import db, Quiz
from run_test import create_app

app = create_app()
app.app_context().push()
db.init_app(app)

from services.quiz.dao.QuizzesDAO import quizCreate, quizRead, quizUpdate, quizDelete
from models import Quiz, User, Staff
from services.core.operations.users_operations import encrypt

class Test_quizzes_dao(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()

        user = User(
            email = 'john_doe@gmail.com',
            encrypted_password=encrypt('password'),
            name = 'john_doe'
        )
        staff = Staff(user)

        db.session.add(staff)
        db.session.commit()

    def test_quizCreate(self):
        
        quiz = Quiz(
            staff_id = 1,
            name = "Quiz Test",
            is_fast = True,
            date_start = '2020-03-01',
            date_end = '2020-03-31',
        )

        quizCreate(quiz)

        quiz_list = Quiz.query.all()

        self.assertEqual(1, len(quiz_list))
        self.assertEqual(quiz_list[0].name, 'Quiz Test')


    def test_quizRead(self):
        
        quiz = Quiz(
            staff_id = 1,
            name = "Quiz Test",
            is_fast = True,
            date_start = '2020-03-01',
            date_end = '2020-03-31',
        )

        db.session.add(quiz)
        db.session.commit()

        quiz_list = Quiz.query.all()

        self.assertEqual(1, len(quiz_list))
        self.assertTrue(quizRead(1))


    def test_quizUpdate(self):
        
        quiz = Quiz(
            staff_id = 1,
            name = "Quiz Test",
            is_fast = True,
            date_start = '2020-03-01',
            date_end = '2020-03-31',
        )

        db.session.add(quiz)
        db.session.commit()

        name_original = quiz.name
        quiz.name = "Quiz Test 2"

        quizUpdate()

        quiz = Quiz.query.filter_by(name='Quiz Test 2').first()
        self.assertNotEqual(name_original, quiz.name)


    def test_quizDelete(self):
        
        quiz = Quiz(
            staff_id = 1,
            name = "Quiz Test",
            is_fast = True,
            date_start = '2020-03-01',
            date_end = '2020-03-31',
        )

        db.session.add(quiz)
        db.session.commit()

        self.assertEqual(1, len(Quiz.query.all()))

        quizDelete(1)

        self.assertEqual(0, len(Quiz.query.all()))


if __name__ == '__main__':
    unittest.main()
