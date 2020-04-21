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

from services.quiz.contracts.questions_contracts import (
    validate_description, 
    validate_id, 
    questionCreateContract, 
    questionDeleteContract, 
    questionReadContract, 
    questionUpdateContract
)
    

"""
This is a TestCase object to test the functions in questions_contracts.py
"""
class Test_questions_contracts(unittest.TestCase):
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

    # test the function validate_description
    def test_validate_description(self):
        print('\r')

        # check if TypeError raised when arg is None type
        print('--- test if arg is None type')
        self.assertRaises(TypeError, validate_description, None)

        # check if ValueError raised when arg is empty string
        print('--- test if arg is empty string')
        self.assertRaises(ValueError, validate_description, '')

    # test the function questionReadContract
    def test_questionReadContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?id=2', method='GET'):
            # check res returned by func is correct
            self.assertEqual(
                questionReadContract(request), 
                {
                    'id': 2
                }
            )

        # passing request with unacceptable value in params (no value passed into 'id')
        print('--- test request with unacceptable params value (no value for \'id\')')
        with app.test_request_context('/?id=', method='GET'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, questionReadContract, request)

    # test the function questionCreateContract
    def test_questionCreateContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?topic_id=1&lesson_id=2&description=hard', method='POST'):
            # check res returned by func is correct
            self.assertEqual(
                questionCreateContract(request), 
                {
                    'topic_id': 1,
                    'lesson_id': 2,
                    'description': 'hard'
                }
            )

        # passing request with unacceptable value in params (empty string passed into 'description')
        print('--- test request with unacceptable params value (empty string for \'description\')')
        with app.test_request_context('/?topic_id=1&lesson_id=2&description=', method='POST'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, questionCreateContract, request)

    # test the function questionUpdateContract
    def test_questionUpdateContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?id=1&description=hard', method='PUT'):
            # check res returned by func is correct
            self.assertEqual(
                questionUpdateContract(request),
                {
                    'id': 1, 
                    'description': 'hard'
                }
            )

        # passing request with unacceptable value in params (empty string passed into 'description')
        print('--- test request with unacceptable params value (empty string for \'description\')')
        with app.test_request_context('/?id=1&description=', method='PUT'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, questionUpdateContract, request)

    # test the function questionDeleteContract
    def test_questionDeleteContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?id=2', method='DELETE'):
            # check res returned by func is correct
            self.assertEqual(
                questionDeleteContract(request),
                {
                    'id': 2
                }
            )

        # passing request with unacceptable value in params (no value passed into 'id')
        print('--- test request with unacceptable params value (no value for \'id\')')
        with app.test_request_context('/?id=', method='DELETE'):
            # check if TyppeError is being raise
            self.assertRaises(TypeError, questionDeleteContract, request)


if __name__ == '__main__':
    unittest.main(verbosity=2)
