import sys
from os import path, getcwd
sys.path.append(getcwd())

from flask import request
import unittest

from models import db
from run_test import create_app

from test_BaseCase import Test_BaseCase, res_to_dict


class Test_questionAttemptsController(Test_BaseCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    
    def test_QuestionAttemptListAPI_GET(self):

        # invalid params input
        response = self.app.get('question_attempts/list?student_id=1&question_id=')
        self.assertEqual(response.status_code, 400)

        # record not found
        response = self.app.get('question_attempts/list?student_id=2&question_id=1')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res['list']), 0)
        
        # success case
        response = self.app.get('question_attempts/list?student_id=1&question_id=1')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['list'][0]['duration_ms'], 10)
        self.assertEqual(len(res['list']), 2)
        

    def test_QuestionAttemptAPI_POST(self):

        # invalid params input
        response = self.app.post('question_attempts?student_id=1&question_id=1&is_correct=true*duration_ms=')
        self.assertEqual(response.status_code, 400)

        # success case
        response = self.app.post('question_attempts?student_id=1&question_id=1&is_correct=true&duration_ms=50')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['duration_ms'], 50)



if __name__ == '__main__':
    unittest.main()
    