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

from services.core.contracts.rs_lesson_quiz_contains_contracts import (
    validate_id, 
    quizMngCreateContract, 
    quizMngReadContract, 
    quizMngDeleteContract
)


"""
This is a TestCase object to test the functions in rs_lesson_quiz_contains_contracts.py
"""
class Test_rs_lesson_quiz_contains_contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # test the function validate_id
    def test_validate_id(self):
        print('\r')

        # check if TypeError raised when arg is None type
        print('--- test if arg is None type')
        self.assertRaises(TypeError, validate_id, None)

        # check if TypeError raised when arg is string type
        print('--- test if arg is string type')
        self.assertRaises(TypeError, validate_id, 'testing')

        # check if TypeError raised when arg is float type
        print('--- test if arg is float type')
        self.assertRaises(TypeError, validate_id, 1.1)

        # check if TypeError raised when arg is boolean type
        print('--- test if arg is boolean type')
        self.assertRaises(TypeError, validate_id, True)

    # test the function quizMngReadContract
    def test_quizMngReadContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?topic_id=1&lesson_id=1', method='GET'):
            # check res returned by func is correct
            self.assertEqual(
                quizMngReadContract(request), 
                {
                    'topic_id': 1,
                    'lesson_id': 1
                }
            )

        # passing request with unacceptable value in params (string type passed in)
        print('--- test request with unacceptable params value (string type for \'lesson_id\')')
        with app.test_request_context('/?topic_id=1&lesson_id=hello', method='GET'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, quizMngReadContract, request)

        # passing request with unacceptable value in params (no value passed into 'lesson_id')
        print('--- test request with unacceptable params value (no value for \'lesson_id\')')
        with app.test_request_context('/?topic_id=1&lesson_id=', method='GET'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, quizMngReadContract, request)

        # passing request with missing params ('lesson_id' param missing)
        print('--- test request with missing params (\'lesson_id\')')
        with app.test_request_context('/?topic_id=1', method='GET'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, quizMngReadContract, request)

    # test the function quizMngCreateContract
    def test_quizMngCreateContract(self):
        print('\r')
        
        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?topic_id=1&lesson_id=1&quiz_id=1', method='POST'):
            # check res returned by func is correct
            self.assertEqual(
                quizMngCreateContract(request), 
                {
                    'topic_id': 1,
                    'lesson_id': 1,
                    'quiz_id': 1
                }
            )

        # passing request with unacceptable value in params (string type passed in)
        print('--- test request with unacceptable params value (string type for \'quiz_id\')')
        with app.test_request_context('/?topic_id=1&lesson_id=1&quiz_id=hello', method='POST'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, quizMngCreateContract, request)

        # passing request with unacceptable value in params (no value passed into 'quiz_id')
        print('--- test request with unacceptable params value (no value for \'quiz_id\')')
        with app.test_request_context('/?topic_id=1&lesson_id=1&quiz_id=', method='POST'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, quizMngCreateContract, request)

        # passing request with missing params ('quiz_id' param missing)
        print('--- test request with missing params (\'quiz_id\')')
        with app.test_request_context('/?topic_id=1&lesson_id=1', method='POST'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, quizMngCreateContract, request)

    # test the function quizMngDeleteContract
    def test_quizMngDeleteContract(self):
        print('\r')
        
        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?id=1', method='DELETE'):
            # check res returned by func is correct
            self.assertEqual(
                quizMngDeleteContract(request), 
                {
                    'id': 1
                }
            )

        # passing request with unacceptable value in params (string type passed in)
        print('--- test request with unacceptable params value (string type for \'id\')')
        with app.test_request_context('/?id=hello', method='DELETE'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, quizMngDeleteContract, request)

        # passing request with unacceptable value in params (no value passed into 'id')
        print('--- test request with unacceptable params value (no value for \'id\')')
        with app.test_request_context('/?id=', method='DELETE'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, quizMngDeleteContract, request)


if __name__ == '__main__':
    unittest.main(verbosity=2)
