import sys
from os import path, getcwd
from flask import Flask
from flask import request
sys.path.append(getcwd())

import unittest

from services.core.contracts.quizAttempts_contracts import *


class Test_quizAttempts_contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def test_validate_student_id(self):
        with self.assertRaises(TypeError):
            validate_student_id(None)

        with self.assertRaises(ValueError):
            validate_student_id("")

    def test_validate_quiz_id(self):
        with self.assertRaises(TypeError):
            validate_quiz_id(None)

        with self.assertRaises(ValueError):
            validate_quiz_id("")

    def test_validate_score(self):
        with self.assertRaises(TypeError):
            validate_score(None)

        with self.assertRaises(ValueError):
            validate_score("")
            validate_score(-7)

    def test_quizAttemptCreateContract(self):
        app = Flask(__name__)
        with app.test_request_context('/?student_id=20&quiz_id=30&score=100', method='POST'):
            self.assertEqual(quizAttemptCreateContract(request), {  'student_id': '20',
        'quiz_id': '30',
        'score': '100'})
        #test not passed as it throws a TypeError since duration_ms is not integer in validate_duration_ms()

        with app.test_request_context('/?student_id=20&quiz_id=30&score=-10', method='POST'):
            # now you can do something with the request until the
            # end of the with block, such as basic assertions:
            # assert request.path == '/hello'
            with self.assertRaises(ValueError):
                quizAttemptCreateContract(request)

    def test_quizAttemptListReadContract(self):
        app = Flask(__name__)
        with app.test_request_context('/?student_id=20&quiz_id=30', method='POST'):
            self.assertEqual(quizAttemptListReadContract(request), {'student_id': '20',
                                                                  'quiz_id': '30'})
        # test not passed as it throws a TypeError since duration_ms is not integer in validate_duration_ms()

        with app.test_request_context('/?student_id=20&quiz_id=', method='POST'):
            # now you can do something with the request until the
            # end of the with block, such as basic assertions:
            # assert request.path == '/hello'
            with self.assertRaises(ValueError):
                quizAttemptListReadContract(request)


if __name__ == '__main__':
    unittest.main()
