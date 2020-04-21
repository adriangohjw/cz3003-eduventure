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

from services.core.contracts.users_contracts import (
    validate_email, 
    validate_password,
    userReadContract,
    userCreateContract,
    userUpdateContract
)
    

"""
This is a TestCase object to test the functions in user_contracts.py
"""
class Test_user_contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls,):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # test the function validate_email
    def test_validate_email(self):
        print('\r')

        # check if TypeError raised when arg is None type
        print('--- test if arg is None type')
        self.assertRaises(TypeError, validate_email, None)
        
        # check if ValueError raised when arg is None type
        print('--- test if arg is empty string')
        self.assertRaises(ValueError, validate_email, '')

        # check if ValueError raised when arg is an email address with no username
        print('--- test if arg is an email address with no username')
        self.assertRaises(ValueError, validate_email, '@gmail.com')

        # check if ValueError raised when arg is an email address with no '@'
        print('--- test if arg is an email address with no \'@\'')
        self.assertRaises(ValueError, validate_email, 'johndoegmail.com')

        # check if ValueError raised when arg is an email address with a domain without a '.'
        print('--- test if arg is an email address with a domain without a \'.\'')
        self.assertRaises(ValueError, validate_email, 'johndoe@gmailcom')

    # test the function validate_password
    def test_validate_password(self):
        print('\r')

        # check if TypeError raised when arg is None type
        print('--- test if arg is None type')
        self.assertRaises(TypeError, validate_password, None)

        # check if ValueError raised when arg is empty string
        print('--- test if arg is empty string')
        self.assertRaises(ValueError, validate_password, '')
            
    # test the function userReadContract
    def test_userReadContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?email=john_doe@gmail.com', method='GET'):
            # check res returned by func is correct
            self.assertEqual(
                userReadContract(request), 
                {
                    'email': "john_doe@gmail.com"
                }
            )

        # passing request with unacceptable value in params (email lacking '@')
        print('--- test request with unacceptable params value (\'email\' lacking \'@\')')
        with app.test_request_context('/?email=johndoegmail.com', method='GET'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, userReadContract, request)

        # passing request with unacceptable value in params (empty string passed in)
        print('--- test request with unacceptable params value (empty string for \'email\')')
        with app.test_request_context('/?email=', method='GET'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, userReadContract, request)

    # test the function userCreateContract
    def test_userCreateContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?email=john_doe@gmail.com&password=12345', method='POST'):
            # check res returned by func is correct
            self.assertEqual(
                userCreateContract(request), 
                {
                    'email': "john_doe@gmail.com", 
                    'password': "12345"
                }
            )

        # passing request with missing params ('password' param missing)
        print('--- test request with missing params (\'password\')')
        with app.test_request_context('/?email=john_doe@gmail.com', method='POST'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, userCreateContract, request)

        # passing request with unacceptable value in params (empty string passed in)
        print('--- test request with unacceptable params value (empty string for \'password\')')
        with app.test_request_context('/?email=john_doe@gmail.com&password=', method='POST'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, userCreateContract, request)

    # test the function userUpdateContract
    def test_userUpdateContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?email=john_doe@gmail.com&old_password=12345&new_password=abcde', method='PUT'):
            # check res returned by func is correct
            self.assertEqual(
                userUpdateContract(request), 
                {
                    'email': "john_doe@gmail.com",
                    'old_password':"12345",
                    'new_password':'abcde'
                }
            )

        # passing request with missing params ('new_password' param missing)
        print('--- test request with missing params (\'new_password\')')
        with app.test_request_context('/?email=john_doe@gmail.com&old_password=12345', method='PUT'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, userUpdateContract, request)

        # passing request with unacceptable value in params (empty string passed in)
        print('--- test request with unacceptable params value (empty string for \'new_password\')')
        with app.test_request_context('/?email=john_doe@gmail.com&old_password=12345&new_password=', method='PUT'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, userUpdateContract, request)


if __name__ == '__main__':
    unittest.main(verbosity=2)
    