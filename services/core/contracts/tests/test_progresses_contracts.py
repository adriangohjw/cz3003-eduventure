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

from services.core.contracts.progresses_contracts import (
    validate_student_id,
    progressReadContract
)


"""
This is a TestCase object to test the functions in progresses_contracts.py
"""
class Test_progresses_contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # test the function validate_student_id
    def test_validate_student_id(self):
        print('\r')

        # check if TypeError raised when arg is None type
        print('--- test if arg is None type')
        self.assertRaises(TypeError, validate_student_id, None)

        # check if TypeError raised when arg is string type
        print('--- test if arg is string type')
        self.assertRaises(TypeError, validate_student_id, 'testing')

        # check if TypeError raised when arg is float type
        print('--- test if arg is float type')
        self.assertRaises(TypeError, validate_student_id, 1.1)

        # check if TypeError raised when arg is boolean type
        print('--- test if arg is boolean type')
        self.assertRaises(TypeError, validate_student_id, True)
    
    def test_progressReadContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?student_id=1', method='GET'):
            # check res returned by func is correct
            self.assertEqual(
                progressReadContract(request), 
                {
                    'student_id': 1
                }
            )

        # passing request with unacceptable value in params (string type passed in)
        print('--- test request with unacceptable params value (string type for \'student_id\')')
        with app.test_request_context('/?student_id=hello', method='GET'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, progressReadContract, request)

        # passing request with unacceptable value in params (no value passed into 'student_id')
        print('--- test request with unacceptable params value (no value for \'student_id\')')
        with app.test_request_context('/?student_id=', method='GET'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, progressReadContract, request)


if __name__ == '__main__':
    unittest.main(verbosity=2)
