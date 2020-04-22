import sys
from os import path, getcwd
sys.path.append(getcwd())

from flask import request
import unittest

from models import db
from run_test import create_app

from test_BaseCase import Test_BaseCase, res_to_dict

from services.core.operations.users_operations import authenticate


"""
This is a TestCase object to test the functions in usersController.py
"""
class Test_usersController(Test_BaseCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # test the GET request for UserAPI
    def test_UserAPI_GET(self):

        # request has invalid params input
        response = self.app.get('/users?email=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record not found
        response = self.app.get('/users?email=staff_2@gmail.com')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 409)
        
        # success cass
        response = self.app.get('/users?email=staff_1@gmail.com')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['name'], 'staff_1')
        
    # test the POST request for UserAPI
    def test_UserAPI_POST(self):

        # request has invalid params input
        response = self.app.post('/users?email=staff_2@gmail.com&password=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record already exist
        response = self.app.post('/users?email=staff_1@gmail.com&password=password')
        # check if status code is correct
        print('--- check if status code is correct (record already exist)')
        self.assertEqual(response.status_code, 409)

        # success case
        response = self.app.post('/users?email=staff_2@gmail.com&password=password')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['name'], 'staff_2')

    # test the PUT request for UserAPI
    def test_UserAPI_PUT(self):

        # request provided incorrect password
        response = self.app.put('/users?email=staff_1@gmail.com&old_password=password1&new_password=password2')
        # check if status code is correct
        print('--- check if status code is correct (provided incorrect password)')
        self.assertEqual(response.status_code, 401)

        # request has invalid params input
        response = self.app.put('/users?email=staff_1@gmail.com&old_password=password&new_password=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record not found
        response = self.app.put('/users?email=staff_2@gmail.com&old_password=password&new_password=password')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 409)

        # success case
        response = self.app.put('/users?email=staff_1@gmail.com&old_password=password&new_password=password2')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertTrue(authenticate('password2', res['encrypted_password']))

    # test the GET request for AuthenticationAPI
    def test_AuthenticationAPI_GET(self):

        # request provided incorrect password
        response = self.app.get('/users/auth?email=staff_1@gmail.com&password=password1')
        # check if status code is correct
        print('--- check if status code is correct (provided incorrect password)')
        self.assertEqual(response.status_code, 401)

        # request has invalid params input
        response = self.app.get('/users/auth?email=staff_1@gmail.com&password=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record not found
        response = self.app.get('/users/auth?email=staff_2@gmail.com&password=password')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 409)

        # success case
        response = self.app.get('/users/auth?email=staff_1@gmail.com&password=password')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        # check if JSON returned is correct
        self.assertEqual(response.status_code, 200)
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['name'], 'staff_1')


if __name__ == '__main__':
    unittest.main(verbosity=2)
    