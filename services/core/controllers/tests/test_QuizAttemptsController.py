import sys
from os import path, getcwd
sys.path.append(getcwd())

from flask import request
import unittest

from models import db
from run_test import create_app

from test_BaseCase import Test_BaseCase, res_to_dict


class Test_quizAttemptsController(Test_BaseCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    
    def test_QuizAttemptListAPI_GET(self):

        # invalid params input
        response = self.app.get('quiz_attempts/list?student_id=1&quiz_id=')
        self.assertEqual(response.status_code, 400)

        # record not found
        response = self.app.get('quiz_attempts/list?student_id=1&quiz_id=2')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 409)
        
        # success case
        response = self.app.get('quiz_attempts/list?student_id=1&quiz_id=1')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['list'][0]['score'], 0)
        self.assertEqual(len(res['list']), 1)
        

    def test_QuizAttemptAPI_POST(self):

        # invalid params input
        response = self.app.post('quiz_attempts?student_id=1&quiz_id=1&score=')
        self.assertEqual(response.status_code, 400)

        # success case
        response = self.app.post('quiz_attempts?student_id=1&quiz_id=1&score=100')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['score'], 100)



if __name__ == '__main__':
    unittest.main()
    