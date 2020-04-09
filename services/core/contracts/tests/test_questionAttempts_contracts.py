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

from services.core.contracts.questionAttempts_contracts import \
    validate_is_correct, validate_duration_ms, validate_student_id, validate_question_id, \
    questionAttemptCreateContract, questionAttemptListReadContract


class Test_questionAttempts_contracts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def test_validate_student_id(self):

        with self.assertRaises(TypeError):
            validate_student_id(None)
            validate_student_id("testStr")
            validate_student_id(1.1)

        with self.assertRaises(ValueError):
            validate_student_id("")


    def test_validate_question_id(self):

        with self.assertRaises(TypeError):
            validate_question_id(None)
            validate_question_id("testStr")
            validate_question_id(1.1)

        with self.assertRaises(ValueError):
            validate_question_id("")


    def test_validate_duration_ms(self):

        with self.assertRaises(TypeError):
            validate_duration_ms(None)
            validate_duration_ms("testStr")
            validate_duration_ms(3.5)

        with self.assertRaises(ValueError):
            validate_duration_ms("")
            validate_duration_ms(-4)


    def test_validate_is_correct(self):

        with self.assertRaises(TypeError):
            validate_is_correct(None)
            validate_is_correct("testStr")
            validate_is_correct(1)
            validate_is_correct(1.1)


    def test_questionAttemptListReadContract(self):

        with app.test_request_context('/?student_id=12&question_id=1', method='GET'):
            self.assertEqual(
                questionAttemptListReadContract(request), 
                {
                    'student_id': 12,
                    'question_id': 1
                }
            )

        with app.test_request_context('/?student_id=12&question_id=', method='GET'):
            self.assertRaises(TypeError, questionAttemptListReadContract, request)

        with app.test_request_context('/?student_id=12&question_id=hello', method='GET'):
            self.assertRaises(TypeError, questionAttemptListReadContract, request)


    def test_questionAttemptCreateContract(self):

        with app.test_request_context('/?student_id=12&question_id=1&is_correct=true&duration_ms=20', method='POST'):
            self.assertEqual(
                questionAttemptCreateContract(request), 
                {
                    'student_id': 12,
                    'question_id': 1, 
                    'is_correct': True,
                    'duration_ms': 20
                }
            )

        with app.test_request_context('/?student_id=12&question_id=1&is_correct=true', method='POST'):
            self.assertRaises(TypeError, questionAttemptCreateContract, request)

        with app.test_request_context('/?student_id=12&question_id=1&is_correct=true&duration_ms=33.3', method='POST'):
            self.assertRaises(TypeError, questionAttemptCreateContract, request)

        with app.test_request_context('/?student_id=12&question_id=1&is_correct=true&duration_ms=-5', method='POST'):
            self.assertRaises(ValueError, questionAttemptCreateContract , request)

        with app.test_request_context('/?student_id=12&question_id=1&is_correct=true&duration_ms=hello', method='POST'):
            self.assertRaises(TypeError, questionAttemptCreateContract , request)


if __name__ == '__main__':
    unittest.main()
