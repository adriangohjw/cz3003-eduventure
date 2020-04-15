import sys
from os import path, getcwd
sys.path.append(getcwd())

from flask import request
import unittest

from models import db
from run_test import create_app

from test_BaseCase import Test_BaseCase, res_to_dict


class Test_staffsController(Test_BaseCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def test_StaffAPI_GET(self):

        # invalid params input
        response = self.app.get('/staffs?email=')
        self.assertEqual(response.status_code, 400)

        # record not found
        response = self.app.get('/staffs?email=staff_2@gmail.com')
        self.assertEqual(response.status_code, 409)
        
        # success case
        from models import Staff
        response = self.app.get('/staffs?email=staff_1@gmail.com')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['name'], 'staff_1')

    
    def test_StaffAPI_POST(self):

        # invalid params input
        response = self.app.post('/staffs?email=staff_1@gmail.com&password=')
        self.assertEqual(response.status_code, 400)

        # existing record
        response = self.app.post('/staffs?email=staff_1@gmail.com&password=password&name=staff_1')
        self.assertEqual(response.status_code, 409)

         # success case
        response = self.app.post('/staffs?email=staff_2@gmail.com&password=password&name=staff_2')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['name'], 'staff_2')


    def test_staff_CourseManagerAPI_GET(self):

        # invalid params input
        response = self.app.get('/staffs/courses?email=')
        self.assertEqual(response.status_code, 400)

        # record not found
        response = self.app.get('/staffs/courses?user_email=staff_2@gmail.com')
        self.assertEqual(response.status_code, 409)

        # success case
        response = self.app.get('/staffs/courses?user_email=staff_1@gmail.com')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['name'], 'staff_1')


    def test_staff_CourseManagerAPI_POST(self):

        # invalid params input
        response = self.app.post('/staffs/courses?user_email=staff_1@gmail.com')
        self.assertEqual(response.status_code, 400)

        # dependency record not found
        response = self.app.post('/staffs/courses?user_email=staff_1@gmail.com&course_index=cz1003')
        self.assertEqual(response.status_code, 409)

        # existing record found
        response = self.app.post('/staffs/courses?user_email=staff_1@gmail.com&course_index=cz1005')
        self.assertEqual(response.status_code, 409)

        # success case
        from models import Course
        course_cz1003 = Course('cz1003')
        db.session.add(course_cz1003)
        db.session.commit()

        response = self.app.post('/staffs/courses?user_email=staff_1@gmail.com&course_index=cz1003')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
    