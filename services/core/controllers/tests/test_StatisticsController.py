import sys
from os import path, getcwd
sys.path.append(getcwd())

from flask import request
import unittest

from models import db
from run_test import create_app

from test_BaseCase import Test_BaseCase, res_to_dict


"""
This is a TestCase object to test the functions in statisticsController.py
"""
class Test_statisticsController(Test_BaseCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # test the GET request for StatsAPI
    def test_Stats_API_GET(self):
        
        # success case
        response = self.app.get('/statistics/stat')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('---  successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(
            res,
            {
                "stats": [
                    {
                    "course_index": "cz1005",
                    "quizzes": [
                        {
                        "25th_percentile": 0.0,
                        "75th_percentile": 0.0,
                        "95th_percentile": 0.0,
                        "attempts": [
                            0
                        ],
                        "avg_score": 0,
                        "id": 1,
                        "max_score": 0,
                        "min_score": 0,
                        "name": "quiz_1",
                        "stdev": None
                        },
                        {
                        "25th_percentile": None,
                        "75th_percentile": None,
                        "95th_percentile": None,
                        "attempts": [],
                        "avg_score": None,
                        "id": 2,
                        "max_score": None,
                        "min_score": None,
                        "name": "quiz_2",
                        "stdev": None
                        },
                        {
                        "25th_percentile": 2.25,
                        "75th_percentile": 2.75,
                        "95th_percentile": 2.95,
                        "attempts": [
                            3,
                            2
                        ],
                        "avg_score": 2.5,
                        "id": 3,
                        "max_score": 3,
                        "min_score": 2,
                        "name": "quiz_3",
                        "stdev": 0.71
                        }
                    ]
                    }
                ]
            }
        )

    # test the GET request for LessonCompletionAPI
    def test_Lesson_Completion_API_GET(self):

        # success case
        response = self.app.get('/statistics/lesson_completed')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertTrue(
            {
                "courses": [
                    {
                        "course_index": "cz1005",
                        "progress": [
                            {
                                "lessons": [
                                    {
                                        "count_completed": 0,
                                        "lesson_id": 1,
                                        "lesson_name": "lesson_1"
                                    },
                                    {
                                        "count_completed": 0,
                                        "lesson_id": 2,
                                        "lesson_name": "lesson_2"
                                    },
                                    {
                                        "count_completed": 1,
                                        "lesson_id": 3,
                                        "lesson_name": "lesson_3"
                                    }
                                ],
                                "topic_id": 1,
                                "topic_name": "topic_1"
                            },
                            {
                                "lessons": [
                                    {
                                        "count_completed": 0,
                                        "lesson_id": 1,
                                        "lesson_name": "lesson_4"
                                    }
                                ],
                                "topic_id": 2,
                                "topic_name": "topic_2"
                            }
                        ]
                    },
                    {
                        "course_index": "all",
                        "progress": [
                            {
                                "lessons": [
                                    {
                                        "count_completed": 0,
                                        "lesson_id": 1,
                                        "lesson_name": "lesson_1"
                                    },
                                    {
                                        "count_completed": 0,
                                        "lesson_id": 2,
                                        "lesson_name": "lesson_2"
                                    },
                                    {
                                        "count_completed": 1,
                                        "lesson_id": 3,
                                        "lesson_name": "lesson_3"
                                    }
                                ],
                                "topic_id": 1,
                                "topic_name": "topic_1"
                            },
                            {
                                "lessons": [
                                    {
                                        "count_completed": 0,
                                        "lesson_id": 1,
                                        "lesson_name": "lesson_4"
                                    }
                                ],
                                "topic_id": 2,
                                "topic_name": "topic_2"
                            }
                        ]
                    }
                ]
            }
        )

    # test the GET request for LeaderboardAPI
    def test_LeaderBoard_API_GET(self):

        # success case (return all students if no proper params passed)
        response = self.app.get('/statistics/leaderboard?student_id=')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (no params passed in) check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful (no params passed in) check if JSON returned is correct')
        self.assertEqual(len(res['scores']), 2)

        # success case (no student found)
        response = self.app.get('/statistics/leaderboard?student_id=3')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (params passed in, but no student found) check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful (params passed in, but no student found) check if JSON returned is correct')
        self.assertEqual(
            res,
            {
                "scores": []
            }
        )

        # success case (student found)
        response = self.app.get('/statistics/leaderboard?student_id=1')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (params passed in and student found - 1) check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful (params passed in and student found - 1) check if JSON returned is correct')
        self.assertEqual(res['scores'][0]['score'], 3)

        response = self.app.get('/statistics/leaderboard?student_id=2')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (params passed in and student found - 2) check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful (params passed in and student found - 2) heck if JSON returned is correct')
        self.assertEqual(res['scores'][0]['score'], 2)

    # test the GET request for StudentScoreAPI
    def test_StudentScore_API_GET(self):

        # success case (return all students if no proper params passed)
        response = self.app.get('/statistics/student_score?student_id=')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (no params passed in) check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful (no params passed in) check if JSON returned is correct')
        self.assertEqual(len(res['students']), 2)
        
        # success case (no student found)
        response = self.app.get('/statistics/student_score?student_id=3')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (params passed in, but no student found) check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful (params passed in, but no student found) check if JSON returned is correct')
        self.assertEqual(
            res,
            {
                "students": []
            }
        )
        
        # success case (student found)
        response = self.app.get('/statistics/student_score?student_id=1')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (params passed in and student found - 1) check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful (params passed in and student found - 1) check if JSON returned is correct')
        self.assertEqual(res['students'][0]['name'], 'student_1')
        self.assertEqual(len(res['students'][0]['quizzes']), 2)

        response = self.app.get('/statistics/student_score?student_id=2')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (params passed in and student found - 2) check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful (params passed in and student found - 2) heck if JSON returned is correct')
        self.assertEqual(res['students'][0]['name'], 'student_2')
        self.assertEqual(len(res['students'][0]['quizzes']), 1)

    # test the GET request for CourseScoreAPI
    def test_CourseScore_API_GET(self):

        # success case (return all courses if no proper params passed in)
        response = self.app.get('/statistics/course_score')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (no params passed in) check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful (no params passed in) check if JSON returned is correct')
        self.assertEqual(len(res['courses']), 2)
        self.assertEqual(
            res,
            {
                "courses": [
                    {
                        "course_index": "cz1005",
                        "scores": {
                            "0-10": 1,
                            "11-20": 0,
                            "21-30": 0,
                            "31-40": 0,
                            "41-50": 0,
                            "51-60": 0,
                            "61-70": 1,
                            "71-80": 0,
                            "81-90": 0,
                            "91-100": 1
                        }
                    },
                    {
                        "course_index": "all",
                        "scores": {
                            "0-10": 1,
                            "11-20": 0,
                            "21-30": 0,
                            "31-40": 0,
                            "41-50": 0,
                            "51-60": 0,
                            "61-70": 1,
                            "71-80": 0,
                            "81-90": 0,
                            "91-100": 1
                        }
                    }
                ]
            }
        )

        # success case (no course found)
        response = self.app.get('/statistics/course_score?course_index=')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (params passed in, but no course found) check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful (params passed in, but no course found) check if JSON returned is correct')
        self.assertEqual(
            res,
            {
                "courses": []
            }
        )
        
        # success case (course found)
        response = self.app.get('/statistics/course_score?course_index=cz1005')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (params passed in and course found) check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful (params passed in and course found) check if JSON returned is correct')
        self.assertEqual(res['courses'][0]['course_index'], 'cz1005')
        self.assertEqual(len(res['courses']), 1)
        self.assertEqual(
            res,
            {
                "courses": [
                    {
                        "course_index": "cz1005",
                        "scores": {
                            "0-10": 1,
                            "11-20": 0,
                            "21-30": 0,
                            "31-40": 0,
                            "41-50": 0,
                            "51-60": 0,
                            "61-70": 1,
                            "71-80": 0,
                            "81-90": 0,
                            "91-100": 1
                        }
                    }
                ]
            }
        )

    # test the GET request for ActivityAPI
    def test_Activity_API_GET(self):

        import datetime
        date_today = datetime.date.today()
        date_today_str = date_today.strftime('%Y-%m-%d')
        date_yesterday = datetime.date.today() - datetime.timedelta(days=10)
        date_yesterday_str = date_yesterday.strftime('%Y-%m-%d')
        date_tomorrow = datetime.date.today() + datetime.timedelta(days=10)
        date_tomorrow_str = date_tomorrow.strftime('%Y-%m-%d')

        # success case (no record found)
        response = self.app.get(
            '/statistics/activity?date_start={date_start}&date_end={date_end}&student_id=1'.format(
                date_start = date_yesterday_str,
                date_end = date_yesterday_str
            )
        )
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (no record found) check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful (no record found) check if JSON returned is correct')
        self.assertEqual(len(res['attempts']), 0)

        # success case
        response = self.app.get(
            '/statistics/activity?date_start={date_start}&date_end={date_end}&student_id=1'.format(
                date_start = date_yesterday_str,
                date_end = date_tomorrow_str
            )
        )
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (record found - 1) check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful (record found - 1) check if JSON returned is correct')
        self.assertEqual(res['attempts'][0][date_today_str], 2)

        # success case
        response = self.app.get(
            '/statistics/activity?date_start={date_start}&date_end={date_end}&student_id=1'.format(
                date_start = date_today_str,
                date_end = date_today_str
            )
        )
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (record found - 2) check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful (record found - 2) check if JSON returned is correct')
        self.assertEqual(res['attempts'][0][date_today_str], 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
    