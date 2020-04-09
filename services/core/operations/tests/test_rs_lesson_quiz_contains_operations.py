import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest

from exceptions import ErrorWithCode

from models import db
from run_test import create_app
app = create_app()
app.app_context().push()
db.init_app(app)

from models import Topic, Lesson, Quiz, User, Staff, Rs_lesson_quiz_contain
from services.core.operations.users_operations import encrypt
from services.core.operations.rs_lesson_quiz_contains_operations import \
    initializeRsLessonQuizContain, quizMngCreateOperation, quizMngReadOperation, quizMngDeleteOperation


class Test_rs_lesson_quiz_contains_operations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()

        topic = Topic(name='seng')
        db.session.add(topic)

        lesson = Lesson(topic_id=1, id=1, name='se', content='test')
        db.session.add(lesson)

        user = User('staff@gmail.com', encrypt('password'), 'staff_name')
        staff = Staff(user)
        db.session.add(staff)

        quiz = Quiz(1, 'quiz_name', True, '2020-03-21', '2020-03-22')
        db.session.add(quiz)

        db.session.commit()


    def test_quizMngReadOperation(self):

        with self.assertRaises(ErrorWithCode):
            quizMngReadOperation(1, 1)

        rs = Rs_lesson_quiz_contain(1, 1, 1)
        db.session.add(rs)
        db.session.commit()
        
        with self.assertRaises(ErrorWithCode):
            quizMngReadOperation(1, 2)
            quizMngReadOperation(2, 1)

        self.assertEqual(len(quizMngReadOperation(1, 1)), 1)

    
    def test_quizMngCreateOperation(self):

        self.assertEqual(len(Rs_lesson_quiz_contain.query.all()), 0)

        quizMngCreateOperation(1, 1, 1)

        self.assertEqual(len(Rs_lesson_quiz_contain.query.all()), 1)

    
    def test_quizMngDeleteOperation(self):

        rs = Rs_lesson_quiz_contain(1, 1, 1)
        db.session.add(rs)
        db.session.commit()

        self.assertRaises(ErrorWithCode, quizMngDeleteOperation, 0)

        self.assertEqual(len(Rs_lesson_quiz_contain.query.filter_by(topic_id=1).filter_by(lesson_id=1).filter_by(quiz_id=1).all()), 1)
        
        self.assertTrue(quizMngDeleteOperation(1))

        self.assertEqual(len(Rs_lesson_quiz_contain.query.filter_by(topic_id=1).filter_by(lesson_id=1).filter_by(quiz_id=1).all()), 0)


if __name__ == '__main__':
    unittest.main()
