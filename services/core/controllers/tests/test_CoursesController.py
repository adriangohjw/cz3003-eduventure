import sys
from os import path, getcwd
sys.path.append(getcwd())

from flask import request
import unittest

from models import db, Course
from run_test import create_app

from test_BaseCase import Test_BaseCase, res_to_dict


"""
This is a TestCase object to test the functions in coursesController.py
"""
class Test_coursesController(Test_BaseCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # test the GET request for CourseAPI
    def test_courseAPI_GET(self):

        # request error as record not found
        response = self.app.get('/courses?index=cz3003')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 409)
        
        # success case
        response = self.app.get('/courses?index=cz1005')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['index'], 'cz1005')

    # test the POST request for CourseAPI
    def test_courseAPI_POST(self):

        # request error as record already exist
        response = self.app.post('/courses?index=cz1005')
        # check if status code is correct
        print('--- check if status code is correct (record already exist)')
        self.assertEqual(response.status_code, 409)

        # success case
        response = self.app.post('/courses?index=cz3003')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['index'], 'cz3003')

    # test the GET request for CourseClasslistAPI
    def test_CourseClasslistAPI_GET(self):

        # request error as record not found
        response = self.app.get('/courses/students/all?course_index=cz3003')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 409)

        # success case (students found in class)
        response = self.app.get('/courses/students/all?course_index=cz1005')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (students found in class), check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful (students found in class), check if JSON returned is correct')
        self.assertEqual(len(res['students']), 2)

        # adding courses
        course = Course('cz1003')
        db.session.add(course)
        db.session.commit()

        # success case (students not found in class)
        response = self.app.get('/courses/students/all?course_index=cz1003')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (students not found in class), check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful (students not found in class), check if JSON returned is correct')
        self.assertEqual(len(res['students']), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
    