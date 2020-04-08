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

from services.core.contracts.quizAttempts_contracts import \
    validate_score, validate_quiz_id, validate_student_id, \
    quizAttemptCreateContract, quizAttemptListReadContract


class Test_quizAttempts_contracts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def test_validate_student_id(self):

        with self.assertRaises(TypeError):
            validate_student_id(None)
            validate_student_id(1.1)
            validate_student_id("test")
            validate_student_id(True)

        with self.assertRaises(ValueError):
            validate_student_id("")


    def test_validate_quiz_id(self):

        with self.assertRaises(TypeError):
            validate_quiz_id(None)
            validate_quiz_id(1.1)
            validate_quiz_id("test")
            validate_quiz_id(True)

        with self.assertRaises(ValueError):
            validate_quiz_id("")


    def test_validate_score(self):

        with self.assertRaises(TypeError):
            validate_score(None)
            validate_score(1.1)
            validate_score("test")
            validate_score(True)

        with self.assertRaises(ValueError):
            validate_score("")
            validate_score(-7)


    def test_quizAttemptCreateContract(self):

        with app.test_request_context('/?student_id=20&quiz_id=30&score=100', method='POST'):
            self.assertEqual(
                quizAttemptCreateContract(request), 
                {
                    'student_id': 20,
                    'quiz_id': 30,
                    'score': 100
                }
            )

        with app.test_request_context('/?student_id=20&quiz_id=30', method='POST'):
            self.assertRaises(TypeError, quizAttemptCreateContract, request)

        with app.test_request_context('/?student_id=20&quiz_id=30&score=-10', method='POST'):
            self.assertRaises(ValueError, quizAttemptCreateContract, request)
        
        with app.test_request_context('/?student_id=hello&quiz_id=30&score=100', method='POST'):
            self.assertRaises(TypeError, quizAttemptCreateContract, request)


    def test_quizAttemptListReadContract(self):

        with app.test_request_context('/?student_id=20&quiz_id=30', method='GET'):
            self.assertEqual(
                quizAttemptListReadContract(request),
                {
                    'student_id': 20,
                    'quiz_id': 30
                }
            )

        with app.test_request_context('/?student_id=20', method='GET'):
            self.assertRaises(TypeError, quizAttemptListReadContract, request)
        
        with app.test_request_context('/?student_id=20&quiz_id=', method='GET'):
            self.assertRaises(TypeError, quizAttemptListReadContract, request)

        with app.test_request_context('/?student_id=hello&quiz_id=30', method='GET'):
            self.assertRaises(TypeError, quizAttemptListReadContract, request)


if __name__ == '__main__':
    unittest.main()
