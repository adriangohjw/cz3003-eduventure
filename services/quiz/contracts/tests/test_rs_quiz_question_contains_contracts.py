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

from services.quiz.contracts.rs_quiz_question_contains_contracts import (
    questionMngCreateContract, 
    questionMngReadContract, 
    questionMngDeleteContract
)


"""
This is a TestCase object to test the functions in rs_quiz_question_contains_contracts.py
"""
class Test_rs_quiz_question_contains_contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # test the function questionMngReadContract
    def test_questionMngReadContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?quiz_id=3', method='GET'):
            # check res returned by func is correct
            self.assertEqual(
                questionMngReadContract(request), 
                {
                    'quiz_id': 3
                }
            )

        # passing request with unacceptable value in params (no value passed into 'quiz_id')
        print('--- test request with unacceptable params value (no value for \'quiz_id\')')
        with app.test_request_context('/?quiz_id=', method='GET'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, questionMngReadContract, request)

    # test the function questionMngCreateContract
    def test_questionMngCreateContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?quiz_id=3&question_id=20', method='POST'):
            # check res returned by func is correct
            self.assertEqual(
                questionMngCreateContract(request),
                {
                    'quiz_id': 3,
                    'question_id': 20
                }
            )

        # passing request with unacceptable value in params (no value passed into 'question_id')
        print('--- test request with unacceptable params value (no value for \'question_id\')')
        with app.test_request_context('/?quiz_id=3&question_id=', method='POST'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, questionMngCreateContract, request)

    # test the function questionMngDeleteContract
    def test_questionMngDeleteContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?quiz_id=3&question_id=20', method='POST'):
            # check res returned by func is correct
            self.assertEqual(
                questionMngDeleteContract(request),
                {
                    'quiz_id': 3,
                    'question_id': 20
                }
            )

        # passing request with unacceptable value in params (no value passed into 'question_id')
        print('--- test request with unacceptable params value (no value for \'question_id\')')
        with app.test_request_context('/?quiz_id=3&question_id=', method='POST'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, questionMngCreateContract, request)


if __name__ == '__main__':
    unittest.main(verbosity=2)
