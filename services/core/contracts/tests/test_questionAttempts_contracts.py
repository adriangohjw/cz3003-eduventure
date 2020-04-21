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

from services.core.contracts.questionAttempts_contracts import (
    validate_is_correct, 
    validate_duration_ms, 
    validate_student_id, 
    validate_question_id, \
    questionAttemptCreateContract, 
    questionAttemptListReadContract
)
    

"""
This is a TestCase object to test the functions in questionAttempts_contracts.py
"""
class Test_questionAttempts_contracts(unittest.TestCase):

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

    # test the function validate_question_id
    def test_validate_question_id(self):
        print('\r')

        # check if TypeError raised when arg is None type
        print('--- test if arg is None type')
        self.assertRaises(TypeError, validate_question_id, None)

        # check if TypeError raised when arg is string type
        print('--- test if arg is string type')
        self.assertRaises(TypeError, validate_question_id, 'testing')

        # check if TypeError raised when arg is float type
        print('--- test if arg is float type')
        self.assertRaises(TypeError, validate_question_id, 1.1)

        # check if TypeError raised when arg is boolean type
        print('--- test if arg is boolean type')
        self.assertRaises(TypeError, validate_question_id, True)

    # test the function validate_duration_ms
    def test_validate_duration_ms(self):
        print('\r')

        # check if TypeError raised when arg is None type
        print('--- test if arg is None type')
        self.assertRaises(TypeError, validate_duration_ms, None)

        # check if TypeError raised when arg is string type
        print('--- test if arg is string type')
        self.assertRaises(TypeError, validate_duration_ms, 'testing')

        # check if TypeError raised when arg is float type
        print('--- test if arg is float type')
        self.assertRaises(TypeError, validate_duration_ms, 1.1)

        # check if TypeError raised when arg is boolean type
        print('--- test if arg is boolean type')
        self.assertRaises(TypeError, validate_duration_ms, True)

        # check if ValueError raised when arg is negative integer
        print('--- test if arg is negative')
        self.assertRaises(ValueError, validate_duration_ms, -1)

    # test the function validate_is_correct
    def test_validate_is_correct(self):
        print('\r')

        # check if TypeError raised when arg is None type
        print('--- test if arg is None type')
        self.assertRaises(TypeError, validate_is_correct, None)

        # check if TypeError raised when arg is string type
        print('--- test if arg is string type')
        self.assertRaises(TypeError, validate_is_correct, 'testing')

        # check if TypeError raised when arg is integer type
        print('--- test if arg is float type')
        self.assertRaises(TypeError, validate_is_correct, 1)

        # check if TypeError raised when arg is float type
        print('--- test if arg is float type')
        self.assertRaises(TypeError, validate_is_correct, 1.1)

    # test the function questionAttemptListReadContract
    def test_questionAttemptListReadContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?student_id=12&question_id=1', method='GET'):
            self.assertEqual(
                # check res returned by func is correct
                questionAttemptListReadContract(request), 
                {
                    'student_id': 12,
                    'question_id': 1
                }
            )

        # passing request with unacceptable value in params (no value passed into 'question_id')
        print('--- test request with unacceptable params value (no value for \'question_id\')')
        with app.test_request_context('/?student_id=12&question_id=', method='GET'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, questionAttemptListReadContract, request)

        # passing request with unacceptable value in params (string type passed in)
        print('--- test request with unacceptable params value (string type for \'question_id\')')
        with app.test_request_context('/?student_id=12&question_id=hello', method='GET'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, questionAttemptListReadContract, request)

    # test the function questionAttemptCreateContract
    def test_questionAttemptCreateContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?student_id=12&question_id=1&is_correct=true&duration_ms=20', method='POST'):
            self.assertEqual(
                # check res returned by func is correct
                questionAttemptCreateContract(request), 
                {
                    'student_id': 12,
                    'question_id': 1, 
                    'is_correct': True,
                    'duration_ms': 20
                }
            )

        # passing request with missing params ('duration_ms' param missing)
        print('--- test request with missing params (\'duration_ms\')')
        with app.test_request_context('/?student_id=12&question_id=1&is_correct=true', method='POST'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, questionAttemptCreateContract, request)

        # passing request with unacceptable value in params (float type passed in)
        print('--- test request with unacceptable params value (float type for \'duration_ms\')')
        with app.test_request_context('/?student_id=12&question_id=1&is_correct=true&duration_ms=33.3', method='POST'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, questionAttemptCreateContract, request)

        # passing request with unacceptable value in params (negative value passed in)
        print('--- test request with unacceptable params value (negative value for \'duration_ms\')')
        with app.test_request_context('/?student_id=12&question_id=1&is_correct=true&duration_ms=-5', method='POST'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, questionAttemptCreateContract , request)

        # passing request with unacceptable value in params (string type passed in)
        print('--- test request with unacceptable params value (string type for \'duration_ms\')')
        with app.test_request_context('/?student_id=12&question_id=1&is_correct=true&duration_ms=hello', method='POST'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, questionAttemptCreateContract , request)


if __name__ == '__main__':
    unittest.main(verbosity=2)
