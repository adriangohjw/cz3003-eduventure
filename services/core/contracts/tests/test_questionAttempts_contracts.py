import sys
from os import path, getcwd
from flask import Flask
from flask import request
sys.path.append(getcwd())

import unittest

from services.core.contracts.questionAttempts_contracts import *


class Test_questionAttempts_contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def test_validate_student_id(self):
        with self.assertRaises(TypeError):
            validate_student_id(None)

        with self.assertRaises(ValueError):
            validate_student_id("")

    def test_validate_question_id(self):
        with self.assertRaises(TypeError):
            validate_question_id(None)

        with self.assertRaises(ValueError):
            validate_question_id("")

    def test_validate_duration_ms(self):
        with self.assertRaises(TypeError):
            validate_duration_ms(None)
            validate_duration_ms(3.5)

        with self.assertRaises(ValueError):
            validate_duration_ms("")
            validate_duration_ms(-4)

    def test_validate_is_correct(self):
        with self.assertRaises(TypeError):
            validate_is_correct(None)
            validate_is_correct("testStr")

        with self.assertRaises(ValueError):
            validate_is_correct("")

    def test_questionAttemptListReadContract(self):
        app = Flask(__name__)
        with app.test_request_context('/?student_id=12&question_id=1', method='POST'):
            self.assertEqual(questionAttemptListReadContract(request), {  'student_id': '12',
        'question_id':'1',})

        with app.test_request_context('/?student_id=12&question_id=', method='POST'):
            # now you can do something with the request until the
            # end of the with block, such as basic assertions:
            # assert request.path == '/hello'
            with self.assertRaises(ValueError):
                questionAttemptListReadContract(request)

    def test_questionAttemptCreateContract(self):
        app = Flask(__name__)
        with app.test_request_context('/?student_id=12&question_id=1&is_correct=True&duration_ms=20', method='POST'):
            self.assertEqual(questionAttemptCreateContract(request), {  'student_id': '12',
        'question_id':'1', 'is_correct': True,
        'duration_ms': 20})
        #test not passed as it throws a TypeError since duration_ms is not integer in validate_duration_ms()

        with app.test_request_context('/?student_id=12&question_id=1&is_correct=True&duration_ms=33.3', method='POST'):
            # now you can do something with the request until the
            # end of the with block, such as basic assertions:
            # assert request.path == '/hello'
            with self.assertRaises(TypeError):
                questionAttemptCreateContract(request)

        with app.test_request_context('/?student_id=12&question_id=1&is_correct=True&duration_ms=-5', method='POST'):
            # now you can do something with the request until the
            # end of the with block, such as basic assertions:
            # assert request.path == '/hello'
            with self.assertRaises(ValueError):
                questionAttemptCreateContract(request)

if __name__ == '__main__':
    unittest.main()
