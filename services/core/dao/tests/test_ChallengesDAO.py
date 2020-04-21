import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest

from models import db
from run_test import create_app
app = create_app()
app.app_context().push()
db.init_app(app)

from models import (
    User, Student, Staff, Topic, Lesson, Quiz, Challenge
)
from services.core.operations.users_operations import encrypt
from services.core.dao.ChallengesDAO import (
    challengeCreate, 
    challengeRead, 
    challengeUpdate
)
    

"""
This is a TestCase object to test the functions in ChallengesDAO.py
"""
class Test_ChallengesDAO(unittest.TestCase):
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
        quiz = Quiz(3, 'quiz_1', True, '2020-03-30', '2020-03-31')
        db.session.add(quiz)

        db.session.commit()

    # test the function challengeCreate
    def test_challengeCreate(self):

        # create a new Challenge object
        challenge = Challenge(1, 2, 1)
    
        # add Challenge object to the database
        challengeCreate(challenge)

        # check that the number of record added is correct
        print('--- check that the number of record added is correct')
        self.assertEqual(len(Challenge.query.all()), 1)

        # check that object cannot be added to database if already exist
        print('--- check that object cannot be added to database if already exist')
        challengeCreate(challenge)
        self.assertEqual(len(Challenge.query.all()), 1)

    # test the function challengeRead
    def test_challengeRead(self):

        # check that function returns the right number of result (= 0)
        print('--- check that function returns the right number of result (= 0)')
        self.assertEqual(len(challengeRead(None, None, None, None)), 0)
        self.assertEqual(len(challengeRead(1, 2, 1, None)), 0)

        # create a new Challenge object and add to database
        challenge = Challenge(1, 2, 1)
        db.session.add(challenge)
        db.session.commit()

        # check that function returns the right number of result (= 1)
        print('--- check that function returns the right number of result (= 1)')
        self.assertEqual(len(challengeRead(None, None, None, None)), 1)
        self.assertEqual(len(challengeRead(1, 2, 1, None)), 1)
        self.assertEqual(len(challengeRead(1, 2, None, None)), 1)

    # test the function challengeUpdate
    def test_challengeUpdate(self):

        # create a new Challenge object and add it to the database
        challenge = Challenge(1, 2, 1)
        db.session.add(challenge)
        db.session.commit()

        # update value of Topic object
        Challenge.query.filter_by(from_student_id=1).filter_by(to_student_id=2).filter_by(quiz_id=1).first().is_completed = True
        challengeUpdate()

        # check if value of Topic object has been updated
        print('--- check if value of Topic object has been updated')
        self.assertEqual(
            Challenge.query.filter_by(from_student_id=1).filter_by(to_student_id=2).filter_by(quiz_id=1).first().is_completed,
            True
        )


if __name__ == '__main__':
    unittest.main(verbosity=2)
    