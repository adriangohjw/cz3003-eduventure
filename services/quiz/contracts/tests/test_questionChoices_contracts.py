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

from services.quiz.contracts.questionChoices_contracts import \
    validate_question_id, validate_questionChoice_id, validate_is_correct, validate_description, \
    questionChoiceCreateContract, questionChoiceDeleteContract, questionChoiceReadContract, questionChoiceUpdateContract


class Test_questionChoices_contracts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def test_validate_questionChoice_id(self):

        with self.assertRaises(TypeError):
            validate_questionChoice_id(None)

        with self.assertRaises(ValueError):
            validate_questionChoice_id("")


    def test_validate_description(self):

        with self.assertRaises(TypeError):
            validate_description(None)

        with self.assertRaises(ValueError):
            validate_description("")


    def test_validate_is_correct(self):

        with self.assertRaises(TypeError):
            validate_is_correct(None)
            validate_is_correct("test")
            validate_is_correct(1)
            validate_is_correct(1.1)


    def test_questionChoiceReadContract(self):

        with app.test_request_context('/?question_id=2&questionChoice_id=3', method='GET'):
            self.assertEqual(
                questionChoiceReadContract(request), 
                {
                    'question_id': 2,
                    'questionChoice_id': 3
                }
            )

        with app.test_request_context('/?question_id=2&questionChoice_id=', method='GET'):
            self.assertRaises(TypeError, questionChoiceReadContract, request)


    def test_questionChoiceCreateContract(self):

        with app.test_request_context('/?question_id=2&description=easy&is_correct=true', method='POST'):
            self.assertEqual(
                questionChoiceCreateContract(request), 
                {
                    'question_id': 2,
                    'description': 'easy',
                    'is_correct': True
                }
            )

        with app.test_request_context('/?question_id=2&description=easy&is_correct=', method='POST'):
            self.assertRaises(TypeError, questionChoiceCreateContract, request)


    def test_questionChoiceUpdateContract(self):

        with app.test_request_context('/?question_id=2&questionChoice_id=2&description=test_description&is_correct=true', method='PUT'):
            self.assertEqual(
                questionChoiceUpdateContract(request),
                {
                    'question_id': 2,
                    'questionChoice_id': 2,
                    'description': 'test_description',
                    'is_correct': True
                }
            )

        with app.test_request_context('/?question_id=2&questionChoice_id=2', method='PUT'):
            self.assertRaises(TypeError, questionChoiceUpdateContract, request)

        with app.test_request_context('/?question_id=2&questionChoice_id=2&description=&is_correct=true', method='PUT'):
            self.assertRaises(ValueError, questionChoiceUpdateContract, request)


    def test_questionChoiceDeleteContract(self):

        with app.test_request_context('/?question_id=2&questionChoice_id=3', method='DELETE'):
            self.assertEqual(
                questionChoiceDeleteContract(request),
                {
                    'question_id': 2,
                    'questionChoice_id': 3
                }
            )

        with app.test_request_context('/?question_id=2&questionChoice_id=', method='DELETE'):
            self.assertRaises(TypeError, questionChoiceDeleteContract, request)


if __name__ == '__main__':
    unittest.main()
