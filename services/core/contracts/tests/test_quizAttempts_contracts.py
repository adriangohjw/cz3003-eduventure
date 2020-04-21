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

from services.core.contracts.quizAttempts_contracts import (
    validate_score, 
    validate_quiz_id, 
    validate_student_id, 
    quizAttemptCreateContract, 
    quizAttemptListReadContract
)


"""
This is a TestCase object to test the functions in quizAttempts_contracts.py
"""
class Test_quizAttempts_contracts(unittest.TestCase):
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

    # test the function validate_quiz_id
    def test_validate_quiz_id(self):
        print('\r')

        # check if TypeError raised when arg is None type
        print('--- test if arg is None type')
        self.assertRaises(TypeError, validate_quiz_id, None)

        # check if TypeError raised when arg is string type
        print('--- test if arg is string type')
        self.assertRaises(TypeError, validate_quiz_id, 'testing')

        # check if TypeError raised when arg is float type
        print('--- test if arg is float type')
        self.assertRaises(TypeError, validate_quiz_id, 1.1)

        # check if TypeError raised when arg is boolean type
        print('--- test if arg is boolean type')
        self.assertRaises(TypeError, validate_quiz_id, True)

    # test the function validate_score
    def test_validate_score(self):
        print('\r')

        # check if TypeError raised when arg is None type
        print('--- test if arg is None type')
        self.assertRaises(TypeError, validate_score, None)

        # check if TypeError raised when arg is string type
        print('--- test if arg is string type')
        self.assertRaises(TypeError, validate_score, 'testing')

        # check if TypeError raised when arg is float type
        print('--- test if arg is float type')
        self.assertRaises(TypeError, validate_score, 1.1)

        # check if TypeError raised when arg is boolean type
        print('--- test if arg is boolean type')
        self.assertRaises(TypeError, validate_score, True)

        # check if ValueError raised when arg is negative integer
        print('--- test if arg is negative')
        self.assertRaises(ValueError, validate_score, -1)


    def test_quizAttemptCreateContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?student_id=20&quiz_id=30&score=100', method='POST'):
            # check res returned by func is correct
            self.assertEqual(
                quizAttemptCreateContract(request), 
                {
                    'student_id': 20,
                    'quiz_id': 30,
                    'score': 100
                }
            )

        # passing request with missing params ('score' param missing)
        print('--- test request with missing params (\'score\')')
        with app.test_request_context('/?student_id=20&quiz_id=30', method='POST'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, quizAttemptCreateContract, request)

        # passing request with unacceptable value in params (negative value passed in)
        print('--- test request with unacceptable params value (negative value for \'score\')')
        with app.test_request_context('/?student_id=20&quiz_id=30&score=-10', method='POST'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, quizAttemptCreateContract, request)
        
        # passing request with unacceptable value in params (string type passed in)
        print('--- test request with unacceptable params value (string type for \'student_id\')')
        with app.test_request_context('/?student_id=hello&quiz_id=30&score=100', method='POST'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, quizAttemptCreateContract, request)


    def test_quizAttemptListReadContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?student_id=20&quiz_id=30', method='GET'):
            # check res returned by func is correct
            self.assertEqual(
                quizAttemptListReadContract(request),
                {
                    'student_id': 20,
                    'quiz_id': 30
                }
            )

        # passing request with missing params ('quiz_id' param missing)
        print('--- test request with missing params (\'quiz_id\')')
        with app.test_request_context('/?student_id=20', method='GET'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, quizAttemptListReadContract, request)
        
        # passing request with unacceptable value in params (no value passed into 'quiz_id')
        print('--- test request with unacceptable params value (no value for \'quiz_id\')')
        with app.test_request_context('/?student_id=20&quiz_id=', method='GET'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, quizAttemptListReadContract, request)

        # passing request with unacceptable value in params (string type passed in)
        print('--- test request with unacceptable params value (string type for \'student_id\')')
        with app.test_request_context('/?student_id=hello&quiz_id=30', method='GET'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, quizAttemptListReadContract, request)


if __name__ == '__main__':
    unittest.main(verbosity=2)
