import sys
from os import path, getcwd
sys.path.append(getcwd())

from flask import request
import unittest

from models import db
from run_test import create_app

from test_BaseCase import Test_BaseCase, res_to_dict


"""
This is a TestCase object to test the functions in progressesController.py
"""
class Test_progressesController(Test_BaseCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # test the GET request for ProgressAPI
    def test_ProgressAPI_GET(self):

        # request has invalid params input
        response = self.app.get('/progresses?student_id=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)
        
        # success case
        response = self.app.get('/progresses?student_id=1')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(
            res,
            {
                "topics": [
                    {
                    "completed_lessons": 2,
                    "completion_status": False,
                    "id": 1,
                    'name': 'topic_1',
                    "lessons": [
                        {
                        "completed_quizzes": 1,
                        "completion_status": False,
                        "id": 1,
                        "quizzes": [
                            {
                            "completion_status": False,
                            "id": 1,
                            "max_score": 0,
                            "total_questions": 1
                            },
                            {
                            "completion_status": True,
                            "id": 2,
                            "max_score": 0,
                            "total_questions": 0
                            }
                        ],
                        "total_quizes": 2
                        },
                        {
                        "completed_quizzes": 0,
                        "completion_status": True,
                        "id": 2,
                        "quizzes": [],
                        "total_quizes": 0
                        },
                        {
                        "completed_quizzes": 1,
                        "completion_status": True,
                        "id": 3,
                        "quizzes": [
                            {
                            "completion_status": True,
                            "id": 3,
                            "max_score": 3,
                            "total_questions": 3
                            }
                        ],
                        "total_quizes": 1
                        }
                    ],
                    "total_lessons": 3
                    },
                    {
                    "completed_lessons": 1,
                    "completion_status": True,
                    "id": 2,
                    'name': 'topic_2',
                    "lessons": [
                        {
                        "completed_quizzes": 0,
                        "completion_status": True,
                        "id": 1,
                        "quizzes": [],
                        "total_quizes": 0
                        }
                    ],
                    "total_lessons": 1
                    }
                ]
            }
        )
    

if __name__ == '__main__':
    unittest.main(verbosity=2)
    