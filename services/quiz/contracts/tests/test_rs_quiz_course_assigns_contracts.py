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

from services.quiz.contracts.rs_quiz_course_assigns_contracts import \
    validate_id, validate_index, \
    courseMngCreateContract, courseMngReadContract


class Test_rs_quiz_course_assigns_contracts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def test_courseMngReadContract(self):

        with app.test_request_context('/?quiz_id=3', method='GET'):
            self.assertEqual(
                courseMngReadContract(request),
                {
                    'quiz_id': 3
                }
            )

        with app.test_request_context('/?quiz_id=', method='GET'):
            self.assertRaises(TypeError, courseMngReadContract, request)


    def test_courseMngCreateContract(self):
        
        with app.test_request_context('/?quiz_id=3&course_index=cz3003', method='POST'):
            self.assertEqual(
                courseMngCreateContract(request), 
                {
                    'quiz_id': 3, 
                    'course_index': 'cz3003'
                }
            )

        with app.test_request_context('/?quiz_id=3&course_index=', method='POST'):
            self.assertRaises(ValueError, courseMngCreateContract, request)


if __name__ == '__main__':
    unittest.main()
