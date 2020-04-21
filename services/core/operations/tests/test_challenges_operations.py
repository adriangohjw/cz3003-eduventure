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


from models import (
    User, Student, Staff, Topic, Lesson, Quiz, Challenge, Question, QuestionAttempt
)
from services.core.operations.users_operations import encrypt
from services.core.operations.challenges_operations import (
    challengeCreateOperation, 
    challengeReadOperation, 
    challengeUpdateCompletedOperation
)


"""
This is a TestCase object to test the functions in challenges_operations.py
"""
class Test_challenges_operations(unittest.TestCase):
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
        user_1 = User('student_1@gmail.com', encrypt('password'), 'student_1')
        student_1 = Student(user_1, 'U00000000A')
        db.session.add(student_1)

        user_2 = User('student_2@gmail.com', encrypt('password'), 'student_2')
        student_2 = Student(user_2, 'U00000000B')
        db.session.add(student_2)

        user_3 = User('teacher_1@gmail.com', encrypt('password'), 'teacher_1')
        staff_1 = Staff(user_3)
        db.session.add(staff_1)
                
        # adding topics
        topic = Topic(name='seng')
        db.session.add(topic)

        # adding lessons
        lesson = Lesson(1, 1, 'lesson_1', 'content')
        db.session.add(lesson)

        # adding quizzes
        quiz_1 = Quiz(3, 'quiz_1', True, '2020-03-30', '2020-03-31')
        db.session.add(quiz_1)

        quiz_2 = Quiz(3, 'quiz_2', True, '2020-03-30', '2020-03-31')
        db.session.add(quiz_2)

        # adding questions
        question_1 = Question(1, 1, 'question_1')
        db.session.add(question_1)

        question_2 = Question(1, 1, 'question_2')
        db.session.add(question_2)
        
        question_3 = Question(1, 1, 'question_3')
        db.session.add(question_3)
        
        question_4 = Question(1, 1, 'question_4')
        db.session.add(question_4)

        # adding challenges
        challenge = Challenge(1, 2, 1)
        db.session.add(challenge)

        db.session.commit()

    # test the function challengeReadOperation
    def test_challengeReadOperation(self):
        
        # check that when successful, result returned by function is of the correct type (1)
        print('--- check that when successful, result returned by function is of the correct type (1)')
        self.assertIsNotNone(challengeReadOperation(None, None, None, None))

        # check that when successful, result returned by function is of the correct type (2)
        print('--- check that when successful, result returned by function is of the correct type (2)')
        self.assertIsNotNone(challengeReadOperation(1, 2, 1, None))

        # check that when successful, result returned by function is of the correct type (3)
        print('--- check that when successful, result returned by function is of the correct type (3)')
        self.assertIsNotNone(challengeReadOperation(1, 2, None, None))

    # test the function challengeCreateOperation
    def test_challengeCreateOperation(self):

        # check that error raised when record (to_student_id) does not exist
        print('--- check that error raised when record (to_student_id) does not exist')
        self.assertRaises(ErrorWithCode, challengeCreateOperation, 1, 3)

        # check that error raised when record (from_student_id) does not exist
        print('--- check that error raised when record (from_student_id) does not exist')
        self.assertRaises(ErrorWithCode,challengeCreateOperation, 3, 2)

        # check that error raised when common question attempted by 2 students are less than 3
        print('--- check that error raised when common question attempted by 2 students are less than 3')
        self.assertRaises(ErrorWithCode, challengeCreateOperation, 1, 2)

        # adding question attempts
        qa_1 = QuestionAttempt(1, 1, True, 1000)
        db.session.add(qa_1)
        qa_2 = QuestionAttempt(1, 2, True, 1000)
        db.session.add(qa_2)
        qa_3 = QuestionAttempt(1, 3, True, 1000)
        db.session.add(qa_3)
        qa_4 = QuestionAttempt(2, 1, True, 1000)
        db.session.add(qa_4)
        qa_5 = QuestionAttempt(2, 2, True, 1000)
        db.session.add(qa_5)
        qa_6 = QuestionAttempt(2, 3, True, 1000)
        db.session.add(qa_6)
        
        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(challengeCreateOperation(1, 2)), Challenge)

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(challengeCreateOperation(1, 2).quiz_id, 4)

    # test the function challengeUpdateCompletedOperation
    def test_challengeUpdateCompletedOperation(self):

        # check that error raised when record does not exist
        print('--- check that error raised when record does not exist')
        self.assertRaises(ErrorWithCode, challengeUpdateCompletedOperation, 1, 2, 2, 1)

        # adding challenge
        challenge = Challenge(1, 2, 2)
        db.session.add(challenge)
        db.session.commit()

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        challenge = Challenge.query.filter_by(from_student_id=1).filter_by(to_student_id=2).filter_by(quiz_id=1).first()
        self.assertEqual(challenge.is_completed, False)
        self.assertIsNone(challenge.winner_id)
        
        challengeUpdateCompletedOperation(1, 2, 1, 1)
        challenge = Challenge.query.filter_by(from_student_id=1).filter_by(to_student_id=2).filter_by(quiz_id=1).first()
        self.assertEqual(challenge.is_completed, True)
        self.assertEqual(challenge.winner_id, 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
    