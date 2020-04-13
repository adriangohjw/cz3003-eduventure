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
        self.assertEqual(response.status_code, 404)
        
        # success case
        from models import Staff
        response = self.app.get('/staffs?email=staff_1@gmail.com')
        print(response.data)
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['name'], 'staff_1')

    
    def test_StaffAPI_POST(self):

        # invalid params input
        response = self.app.post('/staffs?email=staff_1@gmail.com&password=')
        self.assertEqual(response.status_code, 400)

        # existing record
        response = self.app.post('/staffs?email=staff_1@gmail.com&password=password&name=staff_1')
        self.assertEqual(response.status_code, 412)

         # success case
        response = self.app.post('/staffs?email=staff_2@gmail.com&password=password&name=staff_2')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['name'], 'staff_2')


if __name__ == '__main__':
    unittest.main()
    