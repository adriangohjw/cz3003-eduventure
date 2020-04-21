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
    Topic, Lesson, Quiz, User, Staff, Rs_lesson_quiz_contain
)
from services.core.operations.users_operations import encrypt
from services.core.dao.RsLessonQuizContainDAO import (
    rsLessonQuizContainCreate, 
    rsLessonQuizContainRead, 
    rsLessonQuizContainDelete
)
    

"""
This is a TestCase object to test the functions in RsLessonQuizContainDAO.py
"""
class Test_RsLessonQuizContainDAO(unittest.TestCase):
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

        # adding topics
        topic = Topic(name='seng')
        db.session.add(topic)

        # adding lessons
        lesson = Lesson(topic_id=1, id=1, name='se', content='test')
        db.session.add(lesson)

        # adding users
        user = User('staff@gmail.com', encrypt('password'), 'staff_name')
        staff = Staff(user)
        db.session.add(staff)

        # adding quizzes
        quiz = Quiz(1, 'quiz_name', True, '2020-03-21', '2020-03-22')
        db.session.add(quiz)

        db.session.commit()

    # test the function rsLessonQuizContainCreate
    def test_rsLessonQuizContainCreate(self):
        
        # create a new relationship object
        rs = Rs_lesson_quiz_contain(1, 1, 1)

        # add relationship object to the database
        rsLessonQuizContainCreate(rs)

        # retrieve all records from the table
        rs_list = Rs_lesson_quiz_contain.query.all()

        # check that the number of record added is correct
        print('--- check that the number of record added is correct')
        self.assertEqual(len(rs_list), 1)

        # check that the value(s) of the relationship object added is correct
        print('--- check that the value(s) of the relationship object added is correct')
        self.assertEqual(rs_list[0].topic_id, 1)

    # test the function rsLessonQuizContainRead
    def test_rsLessonQuizContainRead(self):

        # create a new relationship object and add it to the database
        rs = Rs_lesson_quiz_contain(1, 1, 1)
        db.session.add(rs)
        db.session.commit()
        
        # check that the number of records retrived is correct
        print('--- check that the number of records retrived is correct')
        self.assertEqual(len(rsLessonQuizContainRead(1, 1)), 1)

        # check that the record retrieved is correct
        print('--- check that the record retrieved is correct')
        self.assertEqual(rsLessonQuizContainRead(1, 1)[0].quiz_id, 1)

    # test the function rsLessonDelete
    def test_rsLessonDelete(self):

        # create a new relationship object and add it to the database
        rs = Rs_lesson_quiz_contain(1, 1, 1)
        db.session.add(rs)
        db.session.commit()

        # check that record has been deleted (number of record in database -1)
        print('--- check that record has been deleted (-1 number of record in database)')
        self.assertEqual(len(rsLessonQuizContainRead(1, 1)), 1)
        rsLessonQuizContainDelete(1)
        self.assertEqual(len(rsLessonQuizContainRead(1, 1)), 0)
        

if __name__ == '__main__':
    unittest.main(verbosity=2)
