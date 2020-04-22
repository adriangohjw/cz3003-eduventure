import sys
from os import path, getcwd
sys.path.append(getcwd())

from flask import request
import unittest

from models import db, Course
from run_test import create_app

from test_BaseCase import Test_BaseCase, res_to_dict


"""
This is a TestCase object to test the functions in studentsController.py
"""
class Test_studentsController(Test_BaseCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # test the GET request for StudentAPI
    def test_StudentAPI_GET(self):

        # request has invalid params input
        response = self.app.get('/students?email=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record not found
        response = self.app.get('/students?email=student_3@gmail.com')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 409)
        
        # success case
        response = self.app.get('/students?email=student_1@gmail.com')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['name'], 'student_1')

    # test the POST request for StudentAPI
    def test_StudentAPI_POST(self):

        # request has invalid params input
        response = self.app.post('/students?email=student_1@gmail.com&password=password&matriculation_number=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record already exist
        response = self.app.post('/students?email=student_1@gmail.com&password=password&matriculation_number=U00000000A')
        # check if status code is correct
        print('--- check if status code is correct (record already exist)')
        self.assertEqual(response.status_code, 409)

        # success case
        response = self.app.post('/students?email=student_3@gmail.com&password=password&matriculation_number=U00000000C')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['name'], 'student_3')

    # test the GET request for CourseManagerAPI
    def test_student_CourseManagerAPI_GET(self):

        # request has invalid params input
        response = self.app.get('/students/courses?user_email=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record not found
        response = self.app.get('/students/courses?user_email=student_3@gmail.com')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 409)

        # success case
        response = self.app.get('/students/courses?user_email=student_1@gmail.com')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['name'], 'student_1')

    # test the POST request for CourseManagerAPI
    def test_student_CourseManagerAPI_POST(self):

        # request has invalid params input
        response = self.app.post('/students/courses?user_email=student_1@gmail.com')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as dependency record not found
        response = self.app.post('/students/courses?user_email=student_1@gmail.com&course_index=cz1003')
        # check if status code is correct
        print('--- check if status code is correct (dependency record not found)')
        self.assertEqual(response.status_code, 409)

        # request error as record already exist
        response = self.app.post('/students/courses?user_email=student_1@gmail.com&course_index=cz1005')
        # check if status code is correct
        print('--- check if status code is correct (record already exist)')
        self.assertEqual(response.status_code, 409)

        # adding courses
        course_cz1003 = Course('cz1003')
        db.session.add(course_cz1003)
        db.session.commit()

        # success case
        response = self.app.post('/students/courses?user_email=student_1@gmail.com&course_index=cz1003')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['student_id'], 1)
        self.assertEqual(res['course_index'], 'cz1003')


if __name__ == '__main__':
    unittest.main(verbosity=2)
    