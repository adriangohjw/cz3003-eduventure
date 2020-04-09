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

from services.core.contracts.rs_lesson_quiz_contains_contracts import \
    validate_id, quizMngCreateContract, quizMngReadContract, quizMngDeleteContract


class Test_rs_lesson_quiz_contains_contracts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    
    def test_validate_id(self):

        with self.assertRaises(TypeError):
            validate_id(None)
            validate_id(1.1)
            validate_id("test")
            validate_id(True)

        with self.assertRaises(ValueError):
            validate_id("")


    def test_quizMngReadContract(self):

        with app.test_request_context('/?topic_id=1&lesson_id=1', method='GET'):
            self.assertEqual(
                quizMngReadContract(request), 
                {
                    'topic_id': 1,
                    'lesson_id': 1
                }
            )

        with app.test_request_context('/?topic_id=1&lesson_id=hello', method='GET'):
            self.assertRaises(TypeError, quizMngReadContract, request)

        with app.test_request_context('/?topic_id=1&lesson_id=', method='GET'):
            self.assertRaises(TypeError, quizMngReadContract, request)

        with app.test_request_context('/?topic_id=1', method='GET'):
            self.assertRaises(TypeError, quizMngReadContract, request)


    def test_quizMngCreateContract(self):
        
        with app.test_request_context('/?topic_id=1&lesson_id=1&quiz_id=1', method='POST'):
            self.assertEqual(
                quizMngCreateContract(request), 
                {
                    'topic_id': 1,
                    'lesson_id': 1,
                    'quiz_id': 1
                }
            )

        with app.test_request_context('/?topic_id=1&lesson_id=1&quiz_id=hello', method='POST'):
            self.assertRaises(TypeError, quizMngCreateContract, request)

        with app.test_request_context('/?topic_id=1&lesson_id=1&quiz_id=', method='POST'):
            self.assertRaises(TypeError, quizMngCreateContract, request)

        with app.test_request_context('/?topic_id=1&lesson_id=1', method='POST'):
            self.assertRaises(TypeError, quizMngCreateContract, request)


    def test_quizMngDeleteContract(self):
        
        with app.test_request_context('/?id=1', method='DELETE'):
            self.assertEqual(
                quizMngDeleteContract(request), 
                {
                    'id': 1
                }
            )

        with app.test_request_context('/?id=hello', method='DELETE'):
            self.assertRaises(TypeError, quizMngDeleteContract, request)

        with app.test_request_context('/?id=', method='DELETE'):
            self.assertRaises(TypeError, quizMngDeleteContract, request)


if __name__ == '__main__':
    unittest.main()
