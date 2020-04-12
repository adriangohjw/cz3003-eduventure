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
from services.core.contracts.statistics_contracts import \
    validate_id, \
    studentScoreReadContract, courseScoreReadContract, activityReadContract


class Test_statistics_contracts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def test_studentScoreReadContract(self):

        with app.test_request_context('/?student_id=1', method='GET'):
            self.assertEqual(
                studentScoreReadContract(request), 
                {
                    'student_id': 1
                }
            )

    
    def test_courseScoreReadContract(self):

        with app.test_request_context('/?course_index=cz1003', method='GET'):
            self.assertEqual(
                courseScoreReadContract(request), 
                {
                    'course_index': 'cz1003'
                }
            )

    
    def test_activityReadContract(self):

        with app.test_request_context('/?date_start=2020-03-30&date_end=2020-03-31&student_id=1', method='GET'):
            self.assertEqual(
                activityReadContract(request), 
                {
                    'date_start': datetime.date(2020, 3, 30),
                    'date_end': datetime.date(2020, 3, 31),
                    'student_id': 1
                }
            )

        with app.test_request_context('/?date_start=2020-03-30&date_end=2020-03-31&student_id=', method='GET'):
            self.assertRaises(TypeError, activityReadContract, request)

        with app.test_request_context('/?date_start=2020-03-30&date_end=20-03-31&student_id=1', method='GET'):
            self.assertRaises(ValueError, activityReadContract, request)

        with app.test_request_context('/?date_start=2020-03-30&date_end=2020-03-31', method='GET'):
            self.assertRaises(TypeError, activityReadContract, request)


if __name__ == '__main__':
    unittest.main()
