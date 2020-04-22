import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from services.core.operations.courses_operations import (
    initializeCourse,
    courseCreateOperation,
    courseReadOperation
)

from exceptions import ErrorWithCode

from models import (
    db, User, Course
)
from run_test import create_app

app = create_app()
app.app_context().push()
db.init_app(app)


"""
This is a TestCase object to test the functions in courses_operations.py
"""
class Test_courses_operations(unittest.TestCase):
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

        # adding courses
        c = initializeCourse('cz3003')
        db.session.add(c)

        db.session.commit()

    # test the function courseReadOperation
    def test_courseReadOperation(self):

        # check that error raised when record does not exist
        print('--- check that error raised when record does not exist')
        with self.assertRaises(ErrorWithCode):
            courseReadOperation('cz3007')

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(courseReadOperation('cz3003')), Course)

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(courseReadOperation('cz3003').index, 'cz3003')

    # test the function courseCreateOperation
    def test_courseCreateOperation(self):

        # check that error raised when record already exist
        print('--- check that error raised when record already exist')
        with self.assertRaises(ErrorWithCode):
            courseCreateOperation('cz3003')

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(courseCreateOperation('cz3007')), Course)

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(courseCreateOperation('cz2003').index, 'cz2003')


if __name__ == '__main__':
    unittest.main(verbosity=2)
