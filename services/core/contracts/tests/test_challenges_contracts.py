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

from services.core.contracts.challenges_contracts import (
    validate_student_id,
    validate_winner_id, 
    challengeReadContract, 
    challengeCreateContract, 
    challengeUpdateCompletedContract
)
    

"""
This is a TestCase object to test the functions in challenge_contracts.py
"""
class Test_challenge_contracts(unittest.TestCase):
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

    # test the function validate_winner_id
    def test_validate_winner_id(self):
        print('\r')

        # check if TypeError raised when arg is None type
        print('--- test if winner_id is None type')
        self.assertRaises(TypeError, validate_winner_id, 1, 2, None)

        # check if TypeError raised when arg is string type
        print('--- test if winner_id is string type')
        self.assertRaises(TypeError, validate_winner_id, 1, 2, 'testing')

        # check if TypeError raised when arg is float type
        print('--- test if winner_id is float type')
        self.assertRaises(TypeError, validate_winner_id, 1, 2, 1.1)

        # check if TypeError raised when arg is boolean type
        print('--- test if winner_id is boolean type')
        self.assertRaises(TypeError, validate_winner_id, 1, 2, True)

        # check if ValueError raised when arg is winner_id not equal to from_student_id / to_student_id
        print('--- test if winner_id not equal to from_student_id / to_student_id')
        self.assertRaises(ValueError, validate_winner_id, 1, 2, 3)


    # test the function challengeReadContract
    def test_challengeReadContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?from_student_id=2&to_student_id=3&quiz_id=4&is_completed=true', method='GET'):
            self.assertEqual(
                challengeReadContract(request), 
                {
                    'from_student_id': 2,
                    'to_student_id': 3,
                    'quiz_id': 4,
                    'is_completed': True
                }
            )
            
    # test the function challengeCreateContract
    def test_challengeCreateContract(self):
        print('\r')
        
        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?from_student_id=2&to_student_id=3', method='POST'):
            # check res returned by func is correct
            self.assertEqual(
                challengeCreateContract(request), 
                {
                    'from_student_id': 2,
                    'to_student_id': 3
                }
            )

        # passing request with unacceptable value in params (no value passed into 'to_student_id')
        print('--- test request with unacceptable params value (no value for \'to_student_id\')')
        with app.test_request_context('/?from_student_id=2&to_student_id=', method='POST'):
            self.assertRaises(TypeError, challengeCreateContract, request)

        # passing request with unacceptable value in params (string type passed in)
        print('--- test request with unacceptable params value (string type for \'student_id\')')
        with app.test_request_context('/?from_student_id=2&to_student_id=hello', method='POST'):
            self.assertRaises(TypeError, challengeCreateContract, request)
        
    # test the function challengeUpdateCompletedContract
    def test_challengeUpdateCompletedContract(self):
        print('\r')

        # passing request with acceptable value (with params winner_id)
        print('--- test acceptable request (with params winner_id)')
        with app.test_request_context('/?from_student_id=2&to_student_id=3&quiz_id=4&winner_id=2', method='PUT'):
            # check res returned by func is correct
            self.assertEqual(
                challengeUpdateCompletedContract(request), 
                {
                    'from_student_id': 2,
                    'to_student_id': 3,
                    'quiz_id': 4,
                    'winner_id': 2
                }
            )

        # passing request with acceptable value (no params winner_id)
        print('--- test acceptable request (no params winner_id') 
        with app.test_request_context('/?from_student_id=2&to_student_id=3&quiz_id=4', method='PUT'):
            # check res returned by func is correct
            self.assertEqual(
                challengeUpdateCompletedContract(request), 
                {
                    'from_student_id': 2,
                    'to_student_id': 3,
                    'quiz_id': 4,
                    'winner_id': None
                }
            )

        # passing request with missing params ('to_student_id' param missing)
        print('--- test request with missing params (\'to_student_id\')')
        with app.test_request_context('/?from_student_id=2&to_student_id=3', method='PUT'):
            self.assertRaises(TypeError, challengeUpdateCompletedContract, request)

        # passing request with unacceptable value in params (string type passed in)
        print('--- test request with unacceptable params value (string type for \'quiz_id\')')
        with app.test_request_context('/?from_student_id=2&to_student_id=3&quiz_id=hello', method='PUT'):
            self.assertRaises(TypeError, challengeUpdateCompletedContract, request)

        # check if ValueError raised when arg is winner_id not equal to from_student_id / to_student_id
        print('--- test if winner_id not equal to from_student_id / to_student_id')
        with app.test_request_context('/?from_student_id=2&to_student_id=3&quiz_id=4&winner_id=1', method='PUT'):
            self.assertRaises(ValueError, challengeUpdateCompletedContract, request)


if __name__ == '__main__':
    unittest.main(verbosity=2)
