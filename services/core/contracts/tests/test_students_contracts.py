import sys
from os import path, getcwd
sys.path.append(getcwd())

from flask import request
import unittest

from models import db
from run_test import create_app
app = create_app()
app.app_context().push()
db.init_app(app)

from services.core.contracts.students_contracts import (
    validate_matriculation_number,
    studentCreateContract, 
    studentReadContract
)
    

"""
This is a TestCase object to test the functions in student_contracts.py
"""
class Test_students_contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # test the function validate_matriculation_number
    def test_validate_matriculation_number(self):
        print('\r')

        # check if TypeError raised when arg is None type
        print('--- test if arg is None type')
        self.assertRaises(TypeError, validate_matriculation_number, None)

        # check if ValueError raised when arg is empty string
        print('--- test if arg is empty string')
        self.assertRaises(ValueError, validate_matriculation_number, '')

    # test the function studentReadContract
    def test_studentReadContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?email=joe@gmail.com', method='GET'):
            # check res returned by func is correct
            self.assertEqual(
                studentReadContract(request), 
                {
                    'email': 'joe@gmail.com'
                }
            )

        # passing request with unacceptable value in params (empty string passed into 'email')
        print('--- test request with unacceptable params value (empty string for \'email\')')
        with app.test_request_context('/?email=', method='GET'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, studentReadContract, request)

        # passing request with unacceptable value in params (email lacking '@')
        print('--- test request with unacceptable params value (\'email\' lacking \'@\')')
        with app.test_request_context('/?email=joegmail.com', method='GET'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, studentReadContract, request)

    # test the function studentCreateContract
    def test_studentCreateContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request (No value passed into name params')
        with app.test_request_context('/?email=joe@gmail.com&password=12345&matriculation_number=u1722', method='POST'):
            # check res returned by func is correct
            self.assertEqual(
                studentCreateContract(request), 
                {
                    'email': 'joe@gmail.com',
                    'password': '12345',
                    'matriculation_number': 'u1722',
                    'name': None
                }
            )
        
        # passing request with acceptable value
        print('--- test acceptable request (Value passed into name params')
        with app.test_request_context('/?email=joe@gmail.com&password=12345&matriculation_number=u1722&name=Joe', method='POST'):
            # check res returned by func is correct
            self.assertEqual(
                studentCreateContract(request), 
                {
                    'email': 'joe@gmail.com',
                    'password': '12345',
                    'matriculation_number': 'u1722',
                    'name': 'Joe'
                }
            )

        # passing request with missing params ('matriculation_number' param missing)
        print('--- test request with missing params (\'matriculation_number\')')
        with app.test_request_context('/?email=joe@gmail.com&password=12345', method='POST'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, studentCreateContract, request)

        # passing request with unacceptable value in params (empty string passed into 'name')
        print('--- test request with unacceptable params value (empty string for \'name\')')
        with app.test_request_context('/?email=&password=12345&matriculation_number=U1721134D', method='POST'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, studentCreateContract, request)

        # passing request with unacceptable value in params (empty string passed into 'matriculation_number')
        print('--- test request with unacceptable params value (empty string for \'matriculation_number\')')
        with app.test_request_context('/?email=joegmail.com&password=12345&matriculation_number=', method='POST'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, studentCreateContract, request)


if __name__ == '__main__':
    unittest.main(verbosity=2)
