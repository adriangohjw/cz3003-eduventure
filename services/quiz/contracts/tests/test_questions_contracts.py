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

from services.quiz.contracts.questions_contracts import \
    validate_description, validate_id, validate_lesson_id, validate_topic_id, \
    questionCreateContract, questionDeleteContract, questionReadContract, questionUpdateContract


class Test_questions_contracts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def test_validate_id(self):

        with self.assertRaises(TypeError):
            validate_id(None)

        with self.assertRaises(ValueError):
            validate_id("")


    def test_validate_description(self):

        with self.assertRaises(Exception):
            validate_description(None)
        
        with self.assertRaises(ValueError):
            validate_description("")


    def test_questionReadContract(self):

        with app.test_request_context('/?id=2', method='GET'):
            self.assertEqual(
                questionReadContract(request), 
                {
                    'id': 2
                }
            )

        with app.test_request_context('/?id=', method='GET'):
            self.assertRaises(TypeError, questionReadContract, request)


    def test_questionCreateContract(self):

        with app.test_request_context('/?topic_id=1&lesson_id=2&description=hard', method='POST'):
            self.assertEqual(
                questionCreateContract(request), 
                {
                    'topic_id': 1,
                    'lesson_id': 2,
                    'description': 'hard'
                }
            )

        with app.test_request_context('/?topic_id=1&lesson_id=2&description=', method='POST'):
            self.assertRaises(ValueError, questionCreateContract, request)


    def test_questionUpdateContract(self):

        with app.test_request_context('/?id=1&description=hard', method='PUT'):
            self.assertEqual(
                questionUpdateContract(request),
                {
                    'id': 1, 
                    'description': 'hard'
                }
            )

        with app.test_request_context('/?id=1&description=', method='PUT'):
            self.assertRaises(ValueError, questionUpdateContract, request)


    def test_questionDeleteContract(self):

        with app.test_request_context('/?id=2', method='DELETE'):
            self.assertEqual(
                questionDeleteContract(request),
                {
                    'id': 2
                }
            )

        with app.test_request_context('/?id=', method='DELETE'):
            self.assertRaises(TypeError, questionDeleteContract, request)


if __name__ == '__main__':
    unittest.main()