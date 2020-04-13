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
        self.assertEqual(response.status_code, 404)
        
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
        self.assertEqual(response.status_code, 412)

         # success case
        response = self.app.post('/students?email=student_3@gmail.com&password=password&matriculation_number=U00000000C')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['name'], 'student_3')


if __name__ == '__main__':
    unittest.main()
    