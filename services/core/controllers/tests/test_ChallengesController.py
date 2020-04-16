import sys
from os import path, getcwd
sys.path.append(getcwd())

from flask import request
import unittest

from models import db
from run_test import create_app

from test_BaseCase import Test_BaseCase, res_to_dict


class Test_challengesController(Test_BaseCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    
    def test_challengeAPI_GET(self):

        # invalid params input
        response = self.app.get('/challenges?from_student_id=')
        self.assertEqual(response.status_code, 400)

        # challenge not found
        response = self.app.get('/challenges?from_student_id=2&to_student_id=1&quiz_id=2')
        self.assertEqual(response.status_code, 200)
        
        # success case
        response = self.app.get('/challenges?from_student_id=1&to_student_id=2')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res), 2)
        

    def test_challengeAPI_POST(self):

        # invalid params input
        response = self.app.post('/challenges?from_student_id=1&to_student_id=')
        self.assertEqual(response.status_code, 400)

        # less than 3 common question attempts
        response = self.app.post('/challenges?from_student_id=2&to_student_id=1')
        self.assertEqual(response.status_code, 409)

        # success case
        from models import QuestionAttempt
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

        response = self.app.post('/challenges?from_student_id=2&to_student_id=1')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['from_student_id'], 2)
        self.assertEqual(res['to_student_id'], 1)
        self.assertFalse(res['is_completed'])
        self.assertIsNone(res['winner_id'])

    
    def test_challengeAPI_PUT(self):

        # invalid params input
        response = self.app.put('/challenges?from_student_id=1&to_student_id=2&quiz_id=1&winner_id=')
        self.assertEqual(response.status_code, 400)

        # challenge not found
        response = self.app.put('/challenges?from_student_id=2&to_student_id=1&quiz_id=2&winner_id=2')
        self.assertEqual(response.status_code, 409)

        # success case
        response = self.app.put('/challenges?from_student_id=1&to_student_id=2&quiz_id=1&winner_id=1')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['winner_id'], 1)
        self.assertTrue(res['is_completed'])


if __name__ == '__main__':
    unittest.main()
    