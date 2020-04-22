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

from services.core.contracts.rs_student_course_enrols_contracts import (
    courseMngReadContract, 
    courseMngCreateContract, 
    courseClasslistReadContract
)


"""
This is a TestCase object to test the functions in rs_student_course_enrols_contracts.py
"""
class Test_rs_student_course_enrols_contracts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # test the function courseMngReadContract
    def test_courseMngReadContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?user_email=joe@gmail.com', method='GET'):
            # check res returned by func is correct
            self.assertEqual(
                courseMngReadContract(request), 
                {
                    'user_email': 'joe@gmail.com'
                }
            )

        # passing request with unacceptable value in params (email lacking '@')
        print('--- test request with unacceptable params value (\'email\' lacking \'@\')')
        with app.test_request_context('/?user_email=joegmail.com', method='GET'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, courseMngReadContract, request)

        # passing request with unacceptable value in params (empty string passed in)
        print('--- test request with unacceptable params value (empty string for \'email\')')
        with app.test_request_context('/?user_email=', method='GET'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, courseMngReadContract, request)

    # test the function courseMngCreateContract
    def test_courseMngCreateContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?user_email=joe@gmail.com&course_index=cz3003', method='POST'):
            # check res returned by func is correct
            self.assertEqual(
                courseMngCreateContract(request), 
                {
                    'user_email': 'joe@gmail.com',
                    'course_index': 'cz3003' 
                }
            )

        # passing request with missing params ('course_index' param missing)
        print('--- test request with missing params (\'course_index\')')
        with app.test_request_context('/?user_email=joe@gmail.com', method='POST'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, courseMngCreateContract, request)

        # passing request with unacceptable value in params (empty string passed in)
        print('--- test request with unacceptable params value (empty string for \'course_index\')')
        with app.test_request_context('/?user_email=joe@gmail.com&course_index=', method='POST'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, courseMngCreateContract, request)

        # passing request with unacceptable value in params (email lacking '@')
        print('--- test request with unacceptable params value (\'email\' lacking \'@\')')
        with app.test_request_context('/?user_email=joegmail.com&course_index=cz3003', method='POST'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, courseMngCreateContract, request)

    # test the function courseClasslistReadContract
    def test_courseClasslistReadContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?course_index=cz3003', method='GET'):
            # check res returned by func is correct
            self.assertEqual(
                courseClasslistReadContract(request), 
                {
                    'course_index': 'cz3003' 
                }
            )

        # passing request with unacceptable value in params (empty string passed in)
        print('--- test request with unacceptable params value (empty string for \'course_index\')')
        with app.test_request_context('/?course_index=', method='GET'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, courseClasslistReadContract, request)


if __name__ == '__main__':
    unittest.main(verbosity=2)
