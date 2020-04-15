import sys
from os import path, getcwd
sys.path.append(getcwd())

from flask import request
import unittest

from models import db
from run_test import create_app

from test_BaseCase import Test_BaseCase, res_to_dict


class Test_studentsController(Test_BaseCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def test_StudentAPI_GET(self):

        # invalid params input
        response = self.app.get('/students?email=')
        self.assertEqual(response.status_code, 400)

        # user not found
        response = self.app.get('/students?email=student_3@gmail.com')
        self.assertEqual(response.status_code, 409)
        
        # success case
        response = self.app.get('/students?email=student_1@gmail.com')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['name'], 'student_1')

    
    def test_StudentAPI_POST(self):

        # invalid params input
        response = self.app.post('/students?email=student_1@gmail.com&password=password&matriculation_number=')
        self.assertEqual(response.status_code, 400)

        # existing record
        response = self.app.post('/students?email=student_1@gmail.com&password=password&matriculation_number=U00000000A')
        self.assertEqual(response.status_code, 409)

         # success case
        response = self.app.post('/students?email=student_3@gmail.com&password=password&matriculation_number=U00000000C')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['name'], 'student_3')

    
    def test_student_CourseManagerAPI_GET(self):

        # invalid params input
        response = self.app.get('/students/courses?user_email=')
        self.assertEqual(response.status_code, 400)

        # record not found
        response = self.app.get('/students/courses?user_email=student_3@gmail.com')
        self.assertEqual(response.status_code, 409)

        # success case
        response = self.app.get('/students/courses?user_email=student_1@gmail.com')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['name'], 'student_1')


    def test_student_CourseManagerAPI_POST(self):

        # invalid params input
        response = self.app.post('/students/courses?user_email=student_1@gmail.com')
        self.assertEqual(response.status_code, 400)

        # dependency record not found
        response = self.app.post('/students/courses?user_email=student_1@gmail.com&course_index=cz1003')
        self.assertEqual(response.status_code, 409)

        # existing record found
        response = self.app.post('/students/courses?user_email=student_1@gmail.com&course_index=cz1005')
        self.assertEqual(response.status_code, 409)

        # success case
        from models import Course
        course_cz1003 = Course('cz1003')
        db.session.add(course_cz1003)
        db.session.commit()

        response = self.app.post('/students/courses?user_email=student_1@gmail.com&course_index=cz1003')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['student_id'], 1)
        self.assertEqual(res['course_index'], 'cz1003')


if __name__ == '__main__':
    unittest.main()
    