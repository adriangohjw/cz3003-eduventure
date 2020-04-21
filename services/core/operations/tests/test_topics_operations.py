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

from services.core.operations.topics_operations import (
    initializeTopic,
    topicCreateOperation,
    topicReadOperation,
    topicUpdateOperation,
    topicDeleteOperation,
    topiclistReadOperation
)
    
from services.core.operations.lessons_operations import (
    initializeLesson
)
from models import Topic


"""
This is a TestCase object to test the functions in topics_operations.py
"""
class Test_topics_operations(unittest.TestCase):
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
        sf = initializeTopic('srs')
        db.session.add(sf)
        db.session.commit()

    # test the function topicReadOperation
    def test_topicReadOperation(self):

        # check that error raised when record does not exist
        print('--- check that error raised when record does not exist')
        with self.assertRaises(ErrorWithCode):
            topicReadOperation(2)

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(topicReadOperation(1)), Topic)

    # test the function topicCreateOperation
    def test_topicCreateOperation(self):

        # check that error raised when record already exist
        print('--- check that error raised when record already exist')
        with self.assertRaises(ErrorWithCode):
            topicCreateOperation('srs')

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(topicCreateOperation('patterns')), Topic)

    # test the function topicUpdateOperation
    def test_topicUpdateOperation(self):

        # check that error raised when record does not exist
        print('--- check that error raised when record does not exist')
        with self.assertRaises(ErrorWithCode):
            topicUpdateOperation(0, 'new_name')

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(topicUpdateOperation(1, 'new_name').name, 'new_name')

    # test the function topicDeleteOperation
    def test_topicDeleteOperation(self):

        # create a new Lesson object and add it to the database
        lesson = initializeLesson(1, 'lesson_1', 'content_1', None)
        db.session.add(lesson)
        db.session.commit()

        # check that error raised when unable to delete record due to dependencies
        print('--- check that error raised when unable to delete record due to dependencies')
        self.assertRaises(ErrorWithCode, topicDeleteOperation, 1)

        # delete dependencies
        db.session.delete(lesson)
        db.session.commit()
        
        # check that record has been deleted (number of record in database -1)
        print('--- check that record has been deleted (-1 number of record in database)')
        self.assertEqual(len(Topic.query.all()), 1)
        self.assertTrue(topicDeleteOperation(1))
        self.assertEqual(len(Topic.query.all()), 0)

    # test the function topiclistReadOperation
    def test_topiclistReadOperation(self):

        # check that function returns the correct number of record (= 1)
        print('--- check that function returns the correct number of record (= 1)')
        self.assertEqual(len(topiclistReadOperation()), 1)
        
        # check that function returns the right result (when number of record = 1)
        print('--- check that function returns the right result (when number of record = 1)')
        self.assertEqual(topiclistReadOperation()[0].name, 'srs')


if __name__ == '__main__':
    unittest.main(verbosity=2)
