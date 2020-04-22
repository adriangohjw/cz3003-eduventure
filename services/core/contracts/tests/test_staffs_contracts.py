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

from services.core.contracts.staffs_contracts import (
    validate_name, 
    staffCreateContract, staffReadContract
)


"""
This is a TestCase object to test the functions in staff_contracts.py
"""
class Test_staffs_contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # test the function validate_name
    def test_validate_name(self):
        print('\r')

        # check if TypeError raised when arg is None type
        print('--- test if arg is None type')
        self.assertRaises(TypeError, validate_name, None)
        
        # check if ValueError raised when arg is None type
        print('--- test if arg is empty string')
        self.assertRaises(ValueError, validate_name, '')

    # test the function staffReadContract
    def test_staffReadContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?email=joe@gmail.com', method='GET'):
            # check res returned by func is correct
            self.assertEqual(
                staffReadContract(request), 
                {
                    'email': 'joe@gmail.com'
                }
            )

        # passing request with unacceptable value in params (email lacking '@')
        print('--- test request with unacceptable params value (\'email\' lacking \'@\')')
        with app.test_request_context('/?email=joegmail.com', method='GET'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, staffReadContract, request)

        # passing request with unacceptable value in params (empty string passed in)
        print('--- test request with unacceptable params value (empty string for \'email\')')
        with app.test_request_context('/?email=', method='GET'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, staffReadContract, request)

    # test the function staffCreateContract
    def test_staffCreateContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?email=joe@gmail.com&password=12345&name=John%20Doe', method='POST'):
            # check res returned by func is correct
            self.assertEqual(
                staffCreateContract(request), 
                {
                    'email': 'joe@gmail.com',
                    'password': '12345',
                    'name': 'John Doe'
                }
            )

        # passing request with unacceptable value in params (email lacking '@')
        print('--- test request with unacceptable params value (\'email\' lacking \'@\')')
        with app.test_request_context('/?email=joegmail.com', method='POST'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, staffCreateContract, request)

        # passing request with unacceptable value in params (empty string passed in)
        print('--- test request with unacceptable params value (empty string for \'email\')')
        with app.test_request_context('/?email=', method='POST'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, staffCreateContract, request)

        # passing request with unacceptable value in params (empty string passed in)
        print('--- test request with unacceptable params value (empty string for \'password\')')
        with app.test_request_context('/?email=joe@gmail.com&password=', method='POST'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, staffCreateContract, request)


if __name__ == '__main__':
    unittest.main(verbosity=2)
