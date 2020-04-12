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


from models import User, Student, Staff, Topic, Lesson, Quiz, Challenge
from services.core.operations.users_operations import encrypt
from services.core.operations.challenges_operations import \
    challengeCreateOperation, challengeReadOperation, challengeUpdateCompletedOperation


class Test_challenges_operations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()

        user_1 = User('student_1@gmail.com', encrypt('password'), 'student_1')
        student_1 = Student(user_1, 'U00000000A')
        db.session.add(student_1)

        user_2 = User('student_2@gmail.com', encrypt('password'), 'student_2')
        student_2 = Student(user_2, 'U00000000B')
        db.session.add(student_2)

        user_3 = User('teacher_1@gmail.com', encrypt('password'), 'teacher_1')
        staff_1 = Staff(user_3)
        db.session.add(staff_1)
                
        topic = Topic(name='seng')
        db.session.add(topic)

        lesson = Lesson(1, 1, 'lesson_1', 'content')
        db.session.add(lesson)

        quiz_1 = Quiz(3, 'quiz_1', True, '2020-03-30', '2020-03-31')
        db.session.add(quiz_1)

        quiz_2 = Quiz(3, 'quiz_2', True, '2020-03-30', '2020-03-31')
        db.session.add(quiz_2)

        challenge = Challenge(1, 2, 1)
        db.session.add(challenge)

        db.session.commit()


    def test_challengeReadOperation(self):
        
        self.assertIsNotNone(challengeReadOperation(None, None, None, None))
        self.assertIsNotNone(challengeReadOperation(1, 2, 1, None))
        self.assertIsNotNone(challengeReadOperation(1, 2, None, None))
        self.assertRaises(ErrorWithCode, challengeReadOperation, 1, 2, 2, None)


    def test_challengeCreateOperation(self):

        self.assertRaises(ErrorWithCode, challengeCreateOperation, 1, 2, 1)

        self.assertEqual(
            len(Challenge.query.filter_by(from_student_id=1).filter_by(to_student_id=2).filter_by(quiz_id=2).all()),
            0
        )

        challengeCreateOperation(1, 2, 2)

        self.assertEqual(
            len(Challenge.query.filter_by(from_student_id=1).filter_by(to_student_id=2).filter_by(quiz_id=2).all()),
            1
        )

        self.assertEqual(
            len(Challenge.query.filter_by(from_student_id=1).all()),
            2
        )


    def test_challengeUpdateCompletedOperation(self):

        self.assertRaises(ErrorWithCode, challengeUpdateCompletedOperation, 1, 2, 2, 1)

        challenge = Challenge(1, 2, 2)
        db.session.add(challenge)
        db.session.commit()

        self.assertEqual(
            Challenge.query.filter_by(from_student_id=1).filter_by(to_student_id=2).filter_by(quiz_id=1).first().is_completed,
            False
        )

        self.assertIsNone(
            Challenge.query.filter_by(from_student_id=1).filter_by(to_student_id=2).filter_by(quiz_id=1).first().winner_id
        )

        challengeUpdateCompletedOperation(1, 2, 1, 1)

        self.assertEqual(
            Challenge.query.filter_by(from_student_id=1).filter_by(to_student_id=2).filter_by(quiz_id=1).first().is_completed,
            True
        )

        self.assertEqual(
            Challenge.query.filter_by(from_student_id=1).filter_by(to_student_id=2).filter_by(quiz_id=1).first().winner_id,
            1
        )

        self.assertEqual(
            Challenge.query.filter_by(from_student_id=1).filter_by(to_student_id=2).filter_by(quiz_id=2).first().is_completed,
            False
        )



if __name__ == '__main__':
    unittest.main()
    