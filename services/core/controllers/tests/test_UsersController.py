import sys
from os import path, getcwd
sys.path.append(getcwd())

from flask import request
import unittest

from models import db
from run_test import create_app

from test_BaseCase import Test_BaseCase, res_to_dict

from services.core.operations.users_operations import authenticate


class Test_usersController(Test_BaseCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    
    def test_UserAPI_GET(self):

        # invalid params input
        response = self.app.get('/users?email=')
        self.assertEqual(response.status_code, 400)

        # user not found
        response = self.app.get('/users?email=staff_2@gmail.com')
        self.assertEqual(response.status_code, 404)
        
        # success case
        response = self.app.get('/users?email=staff_1@gmail.com')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['name'], 'staff_1')
        

    def test_UserAPI_POST(self):

        # invalid params input
        response = self.app.post('/users?email=staff_2@gmail.com&password=')
        self.assertEqual(response.status_code, 400)

        # existing user
        response = self.app.post('/users?email=staff_1@gmail.com&password=password')
        self.assertEqual(response.status_code, 412)

         # success case
        response = self.app.post('/users?email=staff_2@gmail.com&password=password')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['name'], 'staff_2')

    
    def test_UserAPI_PUT(self):

        # wrong password provided
        response = self.app.put('/users?email=staff_1@gmail.com&old_password=password1&new_password=password2')
        self.assertEqual(response.status_code, 401)

        # invalid params input
        response = self.app.put('/users?email=staff_1@gmail.com&old_password=password&new_password=')
        self.assertEqual(response.status_code, 400)

        # user not found
        response = self.app.put('/users?email=staff_2@gmail.com&old_password=password&new_password=password')
        self.assertEqual(response.status_code, 404)

        # success case
        response = self.app.put('/users?email=staff_1@gmail.com&old_password=password&new_password=password2')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(authenticate('password2', res['encrypted_password']))


    def test_AuthenticationAPI_GET(self):

        # wrong password provided
        response = self.app.get('/users/auth?email=staff_1@gmail.com&password=password1')
        self.assertEqual(response.status_code, 401)

        # invalid params input
        response = self.app.get('/users/auth?email=staff_1@gmail.com&password=')
        self.assertEqual(response.status_code, 400)

        # user not found
        response = self.app.get('/users/auth?email=staff_2@gmail.com&password=password')
        self.assertEqual(response.status_code, 404)

        # success case
        response = self.app.get('/users/auth?email=staff_1@gmail.com&password=password')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['name'], 'staff_1')


if __name__ == '__main__':
    unittest.main()
    