import sys
from os import path, getcwd
sys.path.append(getcwd())

from flask import request
import unittest

from models import db, QuestionAttempt
from run_test import create_app

from test_BaseCase import Test_BaseCase, res_to_dict


"""
This is a TestCase object to test the functions in challengesController.py
"""
class Test_challengesController(Test_BaseCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # test the GET request for ChallengeAPI
    def test_challengeAPI_GET(self):

        # request has invalid params input
        response = self.app.get('/challenges?from_student_id=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record not found
        response = self.app.get('/challenges?from_student_id=2&to_student_id=1&quiz_id=2')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 200)
        
        # success case
        response = self.app.get('/challenges?from_student_id=1&to_student_id=2')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(len(res), 2)
        
    # test the POST request for ChallengeAPI
    def test_challengeAPI_POST(self):

        # request has invalid params input
        response = self.app.post('/challenges?from_student_id=1&to_student_id=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as student shave less than 3 common question attempts
        response = self.app.post('/challenges?from_student_id=2&to_student_id=1')
        # check if status code is correct
        print('--- check if status code is correct (both students have less than 3 common question attempts)')
        self.assertEqual(response.status_code, 409)

        # adding questionAttempts
        qa_1 = QuestionAttempt(1, 1, True, 1000)
        db.session.add(qa_1)
        qa_2 = QuestionAttempt(1, 2, True, 1000)
        db.session.add(qa_2)
        qa_3 = QuestionAttempt(1, 3, True, 1000)
        db.session.add(qa_3)
        qa_4 = QuestionAttempt(2, 1, True, 1000)
        db.session.add(qa_4)
        qa_5 = QuestionAttempt(2, 2, True, 1000)
        db.session.add(qa_5)
        qa_6 = QuestionAttempt(2, 3, True, 1000)
        db.session.add(qa_6)
        db.session.commit()

        # success case
        response = self.app.post('/challenges?from_student_id=2&to_student_id=1')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['from_student_id'], 2)
        self.assertEqual(res['to_student_id'], 1)
        self.assertFalse(res['is_completed'])
        self.assertIsNone(res['winner_id'])

    # test the PUT request for ChallengeAPI
    def test_challengeAPI_PUT(self):

        # request has invalid params input
        response = self.app.put('/challenges?from_student_id=1&to_student_id=2&quiz_id=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record already exist
        response = self.app.put('/challenges?from_student_id=2&to_student_id=1&quiz_id=2&winner_id=2')
        # check if status code is correct
        print('--- check if status code is correct (record already exist)')
        self.assertEqual(response.status_code, 409)

        # success case (without winner_id)
        response = self.app.put('/challenges?from_student_id=1&to_student_id=2&quiz_id=1')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (no winner yet), check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful (no winner yet), check if JSON returned is correct')
        self.assertIsNone(res['winner_id'])
        self.assertTrue(res['is_completed'])

        # success case (with winner_id)
        response = self.app.put('/challenges?from_student_id=1&to_student_id=2&quiz_id=2&winner_id=1')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (winner decided), check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful (winner decided), check if JSON returned is correct')
        self.assertEqual(res['winner_id'], 1)
        self.assertTrue(res['is_completed'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
    