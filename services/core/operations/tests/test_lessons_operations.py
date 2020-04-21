import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest

from exceptions import ErrorWithCode

from models import (
    db, Topic,Lesson
)
from run_test import create_app
app = create_app()
app.app_context().push()
db.init_app(app)

from services.core.operations.lessons_operations import (
    initializeLesson,
    lessonCreateOperation,
    lessonReadOperation,
    lessonDeleteOperation,
    lessonUpdateOperation,
    lessonListReadOperation
)


"""
This is a TestCase object to test the functions in lessons_operations.py
"""
class Test_lessons_operations(unittest.TestCase):
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
        l = initializeLesson(1,'lesson1','srs', 'https://www.google.com')
        db.session.add(l)

        db.session.commit()

    # test the function lessonReadOperation
    def test_lessonReadOperation(self):

        # check that error raised when record does not exist
        print('--- check that error raised when record does not exist')
        with self.assertRaises(ErrorWithCode):
            lessonReadOperation(1,2)

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(lessonReadOperation(1,1)), Lesson)

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(lessonReadOperation(1,1).topic_id, 1)

    # test the function lessonCreateOperation
    def test_lessonCreateOperation(self):

        # check that error raised when record already exist
        print('--- check that error raised when record already exist')
        with self.assertRaises(ErrorWithCode):
            lessonCreateOperation(1,'lesson1','srs','https://www.google.com')

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(lessonCreateOperation(1,"lesson2","patterns",'https://www.google.com')), Lesson)

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(lessonCreateOperation(1,"lesson3","patterns",'https://www.google.com').name, 'lesson3')

    # test the function lessonUpdateOperation
    def test_lessonUpdateOperation(self):

        # check that error raised when record does not exist
        print('--- check that error raised when record does not exist')
        with self.assertRaises(ErrorWithCode):
            lessonUpdateOperation(1,2,"name","patterns")

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(lessonUpdateOperation(1,1,"name","lesson3")), Lesson)

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(lessonUpdateOperation(1,1,"name","new_lesson").name, 'new_lesson')

    # test the function lessonDeleteOperation
    def test_lessonDeleteOperation(self):

        # check that error raised when record does not exist
        print('--- check that error raised when record does not exist')
        with self.assertRaises(ErrorWithCode):
            lessonDeleteOperation(1, 2)

        # check that record has been deleted (number of record in database -1)
        print('--- check that record has been deleted (-1 number of record in database)')
        self.assertEqual(len(Lesson.query.all()), 1)
        self.assertTrue(lessonDeleteOperation(1, 1))
        self.assertEqual(len(Lesson.query.all()), 0)

    # test the function lessonListReadOperation
    def test_lessonListReadOperation(self):

        # check that function returns the correct number of record (= 1)
        print('--- check that function returns the correct number of record (= 1)')
        self.assertEqual(len(lessonListReadOperation()), 1)

        # check that function returns the right result (when number of record = 1)
        print('--- check that function returns the right result (when number of record = 1)')
        self.assertEqual(lessonListReadOperation()[0].name, 'lesson1')


if __name__ == '__main__':
    unittest.main(verbosity=2)
