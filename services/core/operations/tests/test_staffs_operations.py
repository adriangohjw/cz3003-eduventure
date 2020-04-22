import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from services.core.operations.staffs_operations import (
    staffCreateOperation, 
    staffReadOperation,
    initializeStaff
)

from exceptions import ErrorWithCode

from models import db, Staff
from run_test import create_app

app = create_app()
app.app_context().push()
db.init_app(app)


"""
This is a TestCase object to test the functions in staffs_operations.py
"""
class Test_staffs_operations(unittest.TestCase):
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

        # adding staffs
        sf = initializeStaff('john_doe@gmail.com', 'password', 'John Doe')
        db.session.add(sf)
        db.session.commit()

    # test the function staffReadOperation
    def test_staffReadOperation(self):

        # check that error raised when record does not exist
        print('--- check that error raised when record does not exist')
        with self.assertRaises(ErrorWithCode):
            staffReadOperation('john_doe_1@gmail.com')

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(staffReadOperation('john_doe@gmail.com')), Staff)

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(staffReadOperation('john_doe@gmail.com').name, 'John Doe')

    # test the function staffCreateOperation
    def test_staffCreateOperation(self):

        # check that error raised when record already exist
        print('--- check that error raised when record already exist')
        with self.assertRaises(ErrorWithCode):
            staffCreateOperation('john_doe@gmail.com', 'password', 'John Doe')

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(staffCreateOperation('john_doe_2@gmail.com', 'password', 'John Doe Tan')), Staff)

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(
            staffCreateOperation('john_doe_3@gmail.com', 'password', 'John Doe Goh').name,
            'John Doe Goh'
        )

if __name__ == '__main__':
    unittest.main(verbosity=2)
