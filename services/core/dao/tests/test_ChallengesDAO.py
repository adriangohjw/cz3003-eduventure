import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest

from models import db
from run_test import create_app
app = create_app()
app.app_context().push()
db.init_app(app)

from models import User, Student, Staff, Topic, Lesson, Quiz, Challenge
from services.core.operations.users_operations import encrypt
from services.core.dao.ChallengesDAO import \
    challengeCreate, challengeRead, challengeUpdate


class Test_ChallengesDAO(unittest.TestCase):

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

        quiz = Quiz(3, 'quiz_1', True, '2020-03-30', '2020-03-31')
        db.session.add(quiz)

        db.session.commit()


    def test_challengeCreate(self):

        self.assertEqual(len(Challenge.query.all()), 0)

        challenge = Challenge(1, 2, 1)
    
        challengeCreate(challenge)
        self.assertEqual(len(Challenge.query.all()), 1)

        challengeCreate(challenge)
        self.assertEqual(len(Challenge.query.all()), 1)


    def test_challengeRead(self):

        self.assertEqual(len(challengeRead(None, None, None, None)), 0)
        self.assertEqual(len(challengeRead(1, 2, 1, None)), 0)

        challenge = Challenge(1, 2, 1)
        db.session.add(challenge)
        db.session.commit()

        self.assertEqual(len(challengeRead(None, None, None, None)), 1)
        self.assertEqual(len(challengeRead(1, 2, 1, None)), 1)
        self.assertEqual(len(challengeRead(1, 2, None, None)), 1)
        self.assertEqual(len(challengeRead(1, 2, 2, None)), 0)


    def test_challengeUpdate(self):

        challenge = Challenge(1, 2, 1)
        db.session.add(challenge)
        db.session.commit()

        self.assertEqual(
            Challenge.query.filter_by(from_student_id=1).filter_by(to_student_id=2).filter_by(quiz_id=1).first().is_completed,
            False
        )

        Challenge.query.filter_by(from_student_id=1).filter_by(to_student_id=2).filter_by(quiz_id=1).first().is_completed = True
        challengeUpdate()

        self.assertEqual(
            Challenge.query.filter_by(from_student_id=1).filter_by(to_student_id=2).filter_by(quiz_id=1).first().is_completed,
            True
        )


if __name__ == '__main__':
    unittest.main()
    