import sys
from os import path, getcwd
from flask import request
from flask import Flask

sys.path.append(getcwd())

import unittest

from services.quiz.contracts.rs_quiz_course_assigns_contracts import *


class Test_rs_quiz_course_assigns_contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def test_courseMngReadContract(self):
        app = Flask(__name__)
        with app.test_request_context('/?quiz_id=3', method='POST'):
            self.assertEqual(courseMngReadContract(request), { 'quiz_id': '3'})

        with app.test_request_context('/?quiz_id=', method='POST'):
            with self.assertRaises(Exception):
                courseMngReadContract(request)

    def test_courseMngCreateContract(self):
        app = Flask(__name__)
        with app.test_request_context('/?quiz_id=3&course_index=cz3003', method='POST'):
            self.assertEqual(courseMngCreateContract(request), { 'quiz_id': '3', 'course_index':'cz3003'})

        with app.test_request_context('/?quiz_id=3&course_index=', method='POST'):
            with self.assertRaises(Exception):
                courseMngCreateContract(request)

if __name__ == '__main__':
    unittest.main()