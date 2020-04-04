import sys
from os import path, getcwd
from flask import request
from flask import Flask

sys.path.append(getcwd())

import unittest

from services.quiz.contracts.questionChoices_contracts import validate_question_id, validate_questionChoice_id, validate_is_correct, validate_col, validate_description, questionChoiceCreateContract,questionChoiceDeleteContract,questionChoiceReadContract,questionChoiceUpdateContract
from models import db
from run_test import create_app

app = create_app()
app.app_context().push()
db.init_app(app)

class Test_questionChoices_contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def test_validate_question_id(self):
        with self.assertRaises(Exception):
            validate_question_id(None)
            validate_question_id("")

    def test_validate_questionChoice_id(self):
        with self.assertRaises(Exception):
            validate_questionChoice_id(None)
            validate_questionChoice_id("")

    def test_validate_description(self):
        with self.assertRaises(Exception):
            validate_description(None)
            validate_description("")

    def test_validate_col(self):
        with self.assertRaises(Exception):
            validate_col(None)
            validate_col("")
            validate_col("test")

    def test_validate_is_correct(self):
        with self.assertRaises(Exception):
            validate_is_correct(None)
            validate_is_correct("")
            validate_is_correct("test")

    def test_questionChoiceReadContract(self):
        with app.test_request_context('/?question_id=2&questionChoice_id=3', method='POST'):
            self.assertEqual(questionChoiceReadContract(request), { 'question_id': '2',
        'questionChoice_id':'3', })

        with app.test_request_context('/?question_id=2&questionChoice_id=', method='POST'):
            with self.assertRaises(Exception):
                questionChoiceReadContract(request)

    def test_questionChoiceCreateContract(self):
        with app.test_request_context('/?question_id=2&description=easy&is_correct=True', method='POST'):
            self.assertEqual(questionChoiceCreateContract(request), { 'question_id': '2',
        'description': 'easy',
        'is_correct': True })

        with app.test_request_context('/?question_id=2&description=easy&is_correct=test', method='POST'):
            with self.assertRaises(Exception):
                questionChoiceCreateContract(request)

        with app.test_request_context('/?question_id=2&description=easy&is_correct=', method='POST'):
            with self.assertRaises(Exception):
                questionChoiceCreateContract(request)

    def test_questionChoiceUpdateContract(self):
        with app.test_request_context('/?question_id=2&questionChoice_id=2&col=description&value=easy', method='POST'):
            self.assertEqual(questionChoiceUpdateContract(request), { 'question_id':'2',
        'questionChoice_id': '2',
        'col': 'description',
        'value':'easy' })

        with app.test_request_context('/?question_id=2&questionChoice_id=2&col=is_correct&value=True', method='POST'):
            self.assertEqual(questionChoiceUpdateContract(request), { 'question_id':'2',
        'questionChoice_id': '2',
        'col': 'is_correct',
        'value':True })

        with app.test_request_context('/?question_id=2&questionChoice_id=2&col=is_correct&value=test', method='POST'):
            with self.assertRaises(Exception):
                questionChoiceUpdateContract(request)

        with app.test_request_context('/?question_id=2&questionChoice_id=2&col=lala&value=True', method='POST'):
            with self.assertRaises(Exception):
                questionChoiceUpdateContract(request)

        with app.test_request_context('/?question_id=2&questionChoice_id=2&col=description&value=', method='POST'):
            with self.assertRaises(Exception):
                questionChoiceUpdateContract(request)

    def test_questionChoiceDeleteContract(self):
        with app.test_request_context('/?question_id=2&questionChoice_id=3', method='POST'):
            self.assertEqual(questionChoiceDeleteContract(request), {  'question_id': '2',
        'questionChoice_id':'3', })

        with app.test_request_context('/?question_id=2&questionChoice_id=', method='POST'):
            with self.assertRaises(Exception):
                questionChoiceDeleteContract(request)


if __name__ == '__main__':
    unittest.main()
