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

from services.core.contracts.courses_contracts import (
    validate_index, 
    courseCreateContract, 
    courseReadContract
)


"""
This is a TestCase object to test the functions in courses_contracts.py
"""
class Test_courses_contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # test the function validate_index
    def test_validate_index(self):
        print('\r')

        # check if TypeError raised when arg is None type
        print('--- test if arg is None type')
        self.assertRaises(TypeError, validate_index, None)

        # check if ValueError raised when arg is empty string
        print('--- test if arg is empty string')
        self.assertRaises(ValueError, validate_index, '')

    # test the function courseReadContract
    def test_courseReadContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?index=cz3003', method='GET'):
            # check res returned by func is correct
            self.assertEqual(
                courseReadContract(request), 
                {
                    'index': 'cz3003'
                }
            )

        # passing request with unacceptable value in params (empty string passed into 'index')
        print('--- test request with unacceptable params value (empty string for \'index\')')
        with app.test_request_context('/?index=', method='GET'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, courseReadContract, request)

    # test the function courseCreateContract
    def test_courseCreateContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?index=cz3003', method='POST'):
            # check res returned by func is correct
            self.assertEqual(
                courseCreateContract(request), 
                {
                    'index': 'cz3003'
                }
            )

        # passing request with unacceptable value in params (empty string passed into 'index')
        print('--- test request with unacceptable params value (empty string for \'index\')')
        with app.test_request_context('/?index=', method='POST'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, courseCreateContract, request)


if __name__ == '__main__':
    unittest.main(verbosity=2)
