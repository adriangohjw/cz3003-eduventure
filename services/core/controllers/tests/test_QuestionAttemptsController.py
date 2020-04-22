import sys
from os import path, getcwd
sys.path.append(getcwd())

from flask import request
import unittest

from models import db
from run_test import create_app

from test_BaseCase import Test_BaseCase, res_to_dict


"""
This is a TestCase object to test the functions in questionAttemptsController.py
"""
class Test_questionAttemptsController(Test_BaseCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # test the GET request for QuestionAttemptListAPI
    def test_QuestionAttemptListAPI_GET(self):

        # request has invalid params input
        response = self.app.get('question_attempts/list?student_id=1&question_id=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record not found
        response = self.app.get('question_attempts/list?student_id=2&question_id=1')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 409)
        
        # success case
        response = self.app.get('question_attempts/list?student_id=1&question_id=1')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correctha 
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['list'][0]['duration_ms'], 10)
        self.assertEqual(len(res['list']), 2)
        
    # test the POST request for QuestionAttemptAPI
    def test_QuestionAttemptAPI_POST(self):

        # request has invalid params input
        response = self.app.post('question_attempts?student_id=1&question_id=1&is_correct=true*duration_ms=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # success case
        response = self.app.post('question_attempts?student_id=1&question_id=1&is_correct=true&duration_ms=50')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['duration_ms'], 50)


if __name__ == '__main__':
    unittest.main(verbosity=2)
    