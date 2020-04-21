import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from services.core.operations.students_operations import (
    initializeStudent, 
    studentCreateOperation, 
    studentReadOperation
)

from exceptions import ErrorWithCode

from models import db, Student
from run_test import create_app

app = create_app()
app.app_context().push()
db.init_app(app)


"""
This is a TestCase object to test the functions in students_operations.py
"""
class Test_students_operations(unittest.TestCase):
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

        # adding students
        sf = initializeStudent('john_doe@gmail.com', 'password','U1722', 'John Doe')
        db.session.add(sf)
        db.session.commit()

    # test the function studentReadOperation
    def test_studentReadOperation(self):

        # check that error raised when record does not exist
        print('--- check that error raised when record does not exist')
        with self.assertRaises(ErrorWithCode):
            studentReadOperation('john_doe_1@gmail.com')

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(studentReadOperation('john_doe@gmail.com')), Student)
    
    # test the function studentCreateOperation
    def test_studentCreateOperation(self):

        # check that error raised when record already exist
        print('--- check that error raised when record already exist')
        with self.assertRaises(ErrorWithCode):
            studentCreateOperation('john_doe@gmail.com', 'password','U1721', None)

        # check that when successful, result returned by function is of the correct type (name is None)
        print('--- check that when successful, result returned by function is of the correct type (name is None)')
        self.assertEqual(type(studentCreateOperation('john_doe_2@gmail.com', 'password','U1721', None)), Student)

        # check that when successful, result returned by function is of the correct type (name is not None)
        print('--- check that when successful, result returned by function is of the correct type (name is not None)')
        self.assertEqual(type(studentCreateOperation('john_doe_3@gmail.com', 'password','U1723', 'John Doe')), Student)

if __name__ == '__main__':
    unittest.main(verbosity=2)
