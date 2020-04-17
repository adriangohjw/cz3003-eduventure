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

from services.core.contracts.challenges_contracts import \
    validate_winner_id, challengeReadContract, challengeCreateContract, challengeUpdateCompletedContract


class Test_challenge_contracts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def test_validate_winner_id(self):

        self.assertRaises(ValueError, validate_winner_id, 1, 2, 3)


    def test_challengeReadContract(self):

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
            

    def test_challengeCreateContract(self):
        
        with app.test_request_context('/?from_student_id=2&to_student_id=3', method='POST'):
            self.assertEqual(
                challengeCreateContract(request), 
                {
                    'from_student_id': 2,
                    'to_student_id': 3
                }
            )

        with app.test_request_context('/?from_student_id=2&to_student_id=', method='POST'):
            self.assertRaises(TypeError, challengeCreateContract, request)

        with app.test_request_context('/?from_student_id=2&to_student_id=hello', method='POST'):
            self.assertRaises(TypeError, challengeCreateContract, request)
        

    def test_challengeUpdateCompletedContract(self):

        with app.test_request_context('/?from_student_id=2&to_student_id=3&quiz_id=4&winner_id=2', method='PUT'):
            self.assertEqual(
                challengeUpdateCompletedContract(request), 
                {
                    'from_student_id': 2,
                    'to_student_id': 3,
                    'quiz_id': 4,
                    'winner_id': 2
                }
            )

        with app.test_request_context('/?from_student_id=2&to_student_id=3&quiz_id=4', method='PUT'):
            self.assertEqual(
                challengeUpdateCompletedContract(request), 
                {
                    'from_student_id': 2,
                    'to_student_id': 3,
                    'quiz_id': 4,
                    'winner_id': None
                }
            )

        with app.test_request_context('/?from_student_id=2&to_student_id=3', method='PUT'):
            self.assertRaises(TypeError, challengeUpdateCompletedContract, request)

        with app.test_request_context('/?from_student_id=2&to_student_id=3&quiz_id=hello', method='PUT'):
            self.assertRaises(TypeError, challengeUpdateCompletedContract, request)

        with app.test_request_context('/?from_student_id=2&to_student_id=3&quiz_id=4&winner_id=1', method='PUT'):
            self.assertRaises(ValueError, challengeUpdateCompletedContract, request)


if __name__ == '__main__':
    unittest.main()
