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

import datetime
from services.core.contracts.statistics_contracts import (
    validate_id, 
    leaderboardReadContract, 
    studentScoreReadContract, 
    courseScoreReadContract, 
    activityReadContract
)


"""
This is a TestCase object to test the functions in statistic_contracts.py
"""
class Test_statistics_contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # test the function leaderboardReadContract
    def test_leaderboardReadContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?student_id=1', method='GET'):
            # check res returned by func is correct
            self.assertEqual(
                leaderboardReadContract(request), 
                {
                    'student_id': 1
                }
            )

    # test the function studentScoreReadContract
    def test_studentScoreReadContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?student_id=1', method='GET'):
            # check res returned by func is correct
            self.assertEqual(
                studentScoreReadContract(request), 
                {
                    'student_id': 1
                }
            )

    # test the function courseScoreReadContract
    def test_courseScoreReadContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?course_index=cz1003', method='GET'):
            # check res returned by func is correct
            self.assertEqual(
                courseScoreReadContract(request), 
                {
                    'course_index': 'cz1003'
                }
            )

    # test the function activityReadContract
    def test_activityReadContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?date_start=2020-03-30&date_end=2020-03-31&student_id=1', method='GET'):
            # check res returned by func is correct
            self.assertEqual(
                activityReadContract(request), 
                {
                    'date_start': datetime.date(2020, 3, 30),
                    'date_end': datetime.date(2020, 3, 31),
                    'student_id': 1
                }
            )

        # passing request with unacceptable value in params (no value passed into 'student_id')
        print('--- test request with unacceptable params value (no value for \'student_id\')')
        with app.test_request_context('/?date_start=2020-03-30&date_end=2020-03-31&student_id=', method='GET'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, activityReadContract, request)

        # passing request with unacceptable value in params (incorrect format passed into 'date_end')
        print('--- test request with unacceptable params value (incorrect format for \'date_end\')')
        with app.test_request_context('/?date_start=2020-03-30&date_end=20-03-31&student_id=1', method='GET'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, activityReadContract, request)

        # passing request with missing params ('student_id' param missing)
        print('--- test request with missing params (\'student_id\')')
        with app.test_request_context('/?date_start=2020-03-30&date_end=2020-03-31', method='GET'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, activityReadContract, request)


if __name__ == '__main__':
    unittest.main(verbosity=2)
