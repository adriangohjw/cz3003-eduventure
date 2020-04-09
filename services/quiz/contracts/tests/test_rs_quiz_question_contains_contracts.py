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

from services.quiz.contracts.rs_quiz_question_contains_contracts import \
    questionMngCreateContract, questionMngReadContract


class Test_rs_quiz_question_contains_contracts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def test_questionMngReadContract(self):

        with app.test_request_context('/?quiz_id=3', method='GET'):
            self.assertEqual(
                questionMngReadContract(request), 
                {
                    'quiz_id': 3
                }
            )

        with app.test_request_context('/?quiz_id=', method='GET'):
            self.assertRaises(TypeError, questionMngReadContract, request)


    def test_questionMngCreateContract(self):

        with app.test_request_context('/?quiz_id=3&question_id=20', method='POST'):
            self.assertEqual(
                questionMngCreateContract(request),
                {
                    'quiz_id': 3,
                    'question_id': 20
                }
            )

        with app.test_request_context('/?quiz_id=3&question_id=', method='POST'):
            self.assertRaises(TypeError, questionMngCreateContract, request)


if __name__ == '__main__':
    unittest.main()
