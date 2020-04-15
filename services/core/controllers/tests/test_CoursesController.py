import sys
from os import path, getcwd
sys.path.append(getcwd())

from flask import request
import unittest

from models import db
from run_test import create_app

from test_BaseCase import Test_BaseCase, res_to_dict


class Test_coursesController(Test_BaseCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def test_courseAPI_GET(self):

        # record not found
        response = self.app.get('/courses?index=cz3003')
        self.assertEqual(response.status_code, 409)
        
        # success case
        response = self.app.get('/courses?index=cz1005')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['index'], 'cz1005')


    def test_courseAPI_POST(self):

        # existing record
        response = self.app.post('/courses?index=cz1005')
        self.assertEqual(response.status_code, 409)

         # success case
        response = self.app.post('/courses?index=cz3003')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['index'], 'cz3003')


    def test_CourseClasslistAPI_GET(self):

        # record not found
        response = self.app.get('/courses/students/all?course_index=cz3003')
        self.assertEqual(response.status_code, 409)

        # success case (students found in class)
        response = self.app.get('/courses/students/all?course_index=cz1005')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res['students']), 2)

        # success case (students not found in class)
        from models import Course
        course = Course('cz1003')
        db.session.add(course)
        db.session.commit()

        response = self.app.get('/courses/students/all?course_index=cz1003')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res['students']), 0)


if __name__ == '__main__':
    unittest.main()
    