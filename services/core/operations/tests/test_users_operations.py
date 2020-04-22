import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest

from services.core.operations.users_operations import (
    encrypt, 
    authenticate, 
    initializeUser,
    userReadOperation, 
    userCreateOperation, 
    userUpdateOperation,
    authOperation
)

from exceptions import ErrorWithCode

from models import db, User
from run_test import create_app

app = create_app()
app.app_context().push()
db.init_app(app)


"""
This is a TestCase object to test the functions in users_operations.py
"""
class Test_users_operations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # this will run before every test
    # it will ensure that every test start with a fresh database
    def setUp(self):
        print('\r')
        # drop all tables in the database
        db.session.remove()
        db.drop_all()
        # crete all tables in the database
        db.create_all()

        # adding users
        u = initializeUser('john_doe@gmail.com', 'password')
        db.session.add(u)
        db.session.commit()

    # test the function encrypt and authenticate
    def test_encryption(self):

        # check that authenticate function works, with encrypted string
        print('--- check that authenticate function works, with encrypted string')
        plaintext_password = 'random_password'
        encrypted_password = encrypt(plaintext_password)
        self.assertTrue(authenticate(plaintext_password, encrypted_password))

    # test the function userReadOperation
    def test_userReadOperation(self):

        # check that error raised when record does not exist
        print('--- check that error raised when record does not exist')
        with self.assertRaises(ErrorWithCode):
            userReadOperation('john_doe_1@gmail.com')

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(userReadOperation('john_doe@gmail.com')), User)

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(userReadOperation('john_doe@gmail.com').name, 'john_doe')

    # test the function userCreateOperation
    def test_userCreateOperation(self):

        # check that error raised when record already exist
        print('--- check that error raised when record already exist')
        with self.assertRaises(ErrorWithCode):
            userCreateOperation('john_doe@gmail.com', 'password')

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(userCreateOperation('john_doe_2@gmail.com', 'password')), User)

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(userCreateOperation('john_doe_3@gmail.com', 'password').name, 'john_doe_3')

    # test the function userUpdateOperation
    def test_userUpdateOperation(self):

        # check that error raised when record does not exist
        print('--- check that error raised when record does not exist')
        with self.assertRaises(ErrorWithCode):
            userUpdateOperation('john_doe_2@gmail.com', 'password', 'password_new')

        # check that error raised when old_password is wrong
        print('--- check that error raised when old_password is wrong')
        with self.assertRaises(ErrorWithCode):
            userUpdateOperation('john_doe@gmail.com', 'password_wrong', 'password_new')

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(userUpdateOperation('john_doe@gmail.com', 'password', 'password_new')), User)

    # test the function authOperation
    def test_authOperation(self):

        # check that error raised when record does not exist
        print('--- check that error raised when record does not exist')
        with self.assertRaises(ErrorWithCode):
            authOperation('john_doe_1@gmail.com', 'password')

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(authOperation('john_doe@gmail.com', 'password')), User)

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(authOperation('john_doe@gmail.com', 'password').name, 'john_doe')


if __name__ == '__main__':
    unittest.main(verbosity=2)
    