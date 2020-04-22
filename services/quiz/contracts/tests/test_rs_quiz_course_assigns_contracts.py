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

from services.quiz.contracts.rs_quiz_course_assigns_contracts import (
    courseMngCreateContract, 
    courseMngReadContract
)
    

"""
This is a TestCase object to test the functions in rs_quiz_course_assigns_contracts.py
"""
class Test_rs_quiz_course_assigns_contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # test the function courseMngReadContract
    def test_courseMngReadContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?quiz_id=3', method='GET'):
            # check res returned by func is correct
            self.assertEqual(
                courseMngReadContract(request),
                {
                    'quiz_id': 3
                }
            )

        # passing request with unacceptable value in params (no value passed into 'quiz_id')
        print('--- test request with unacceptable params value (no value for \'quiz_id\')')
        with app.test_request_context('/?quiz_id=', method='GET'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, courseMngReadContract, request)

    # test the function courseMngCreateContract
    def test_courseMngCreateContract(self):
        print('\r')
        
        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?quiz_id=3&course_index=cz3003', method='POST'):
            # check res returned by func is correct
            self.assertEqual(
                courseMngCreateContract(request), 
                {
                    'quiz_id': 3, 
                    'course_index': 'cz3003'
                }
            )

        # passing request with unacceptable value in params (no value passed into 'course_index')
        print('--- test request with unacceptable params value (no value for \'course_index\')')
        with app.test_request_context('/?quiz_id=3&course_index=', method='POST'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, courseMngCreateContract, request)


if __name__ == '__main__':
    unittest.main(verbosity=2)
