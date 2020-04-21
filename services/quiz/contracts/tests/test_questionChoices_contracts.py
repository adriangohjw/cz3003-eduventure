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

from services.quiz.contracts.questionChoices_contracts import (
    validate_questionChoice_id, 
    validate_is_correct, 
    validate_description, 
    questionChoiceCreateContract, 
    questionChoiceDeleteContract, 
    questionChoiceReadContract, 
    questionChoiceUpdateContract
)


"""
This is a TestCase object to test the functions in questionChoices_contracts.py
"""
class Test_questionChoices_contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # test the function validate_questionChoice_id
    def test_validate_questionChoice_id(self):
        print('\r')

        # check if TypeError raised when arg is None type
        print('--- test if arg is None type')
        self.assertRaises(TypeError, validate_questionChoice_id, None)

        # check if TypeError raised when arg is string type
        print('--- test if arg is string type')
        self.assertRaises(TypeError, validate_questionChoice_id, 'testing')

        # check if TypeError raised when arg is float type
        print('--- test if arg is float type')
        self.assertRaises(TypeError, validate_questionChoice_id, 1.1)

        # check if TypeError raised when arg is boolean type
        print('--- test if arg is boolean type')
        self.assertRaises(TypeError, validate_questionChoice_id, True)

    # test the function validate_description
    def test_validate_description(self):
        print('\r')

        # check if TypeError raised when arg is None type
        print('--- test if arg is None type')
        self.assertRaises(TypeError, validate_description, None)

        # check if ValueError raised when arg is empty string
        print('--- test if arg is empty string')
        self.assertRaises(ValueError, validate_description, '')

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

    # test the function questionChoiceReadContract
    def test_questionChoiceReadContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?question_id=2&questionChoice_id=3', method='GET'):
            # check res returned by func is correct
            self.assertEqual(
                questionChoiceReadContract(request), 
                {
                    'question_id': 2,
                    'questionChoice_id': 3
                }
            )

        # passing request with unacceptable value in params (no value passed into 'questionChoice_id')
        print('--- test request with unacceptable params value (no value for \'questionChoice_id\')')
        with app.test_request_context('/?question_id=2&questionChoice_id=', method='GET'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, questionChoiceReadContract, request)

    # test the function questionChoiceCreateContract
    def test_questionChoiceCreateContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?question_id=2&description=easy&is_correct=true', method='POST'):
            # check res returned by func is correct
            self.assertEqual(
                questionChoiceCreateContract(request), 
                {
                    'question_id': 2,
                    'description': 'easy',
                    'is_correct': True
                }
            )

        # passing request with unacceptable value in params (no value passed into 'is_correct')
        print('--- test request with unacceptable params value (no value for \'is_correct\')')
        with app.test_request_context('/?question_id=2&description=easy&is_correct=', method='POST'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, questionChoiceCreateContract, request)

    # test the function questionChoiceUpdateContract
    def test_questionChoiceUpdateContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?question_id=2&questionChoice_id=2&description=test_description&is_correct=true', method='PUT'):
            # check res returned by func is correct
            self.assertEqual(
                questionChoiceUpdateContract(request),
                {
                    'question_id': 2,
                    'questionChoice_id': 2,
                    'description': 'test_description',
                    'is_correct': True
                }
            )

        # passing request with missing params ('is_correct' param missing)
        print('--- test request with missing params (\'is_correct\')')
        with app.test_request_context('/?question_id=2&questionChoice_id=2', method='PUT'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, questionChoiceUpdateContract, request)

        # passing request with unacceptable value in params (empty string passed in)
        print('--- test request with unacceptable params value (empty string for \'description\')')
        with app.test_request_context('/?question_id=2&questionChoice_id=2&description=&is_correct=true', method='PUT'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, questionChoiceUpdateContract, request)

    # test the function questionChoiceDeleteContract
    def test_questionChoiceDeleteContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?question_id=2&questionChoice_id=3', method='DELETE'):
            # check res returned by func is correct
            self.assertEqual(
                questionChoiceDeleteContract(request),
                {
                    'question_id': 2,
                    'questionChoice_id': 3
                }
            )

        # passing request with unacceptable value in params (no value passed into 'questionChoice_id')
        print('--- test request with unacceptable params value (no value for \'questionChoice_id\')')
        with app.test_request_context('/?question_id=2&questionChoice_id=', method='DELETE'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, questionChoiceDeleteContract, request)


if __name__ == '__main__':
    unittest.main(verbosity=2)
