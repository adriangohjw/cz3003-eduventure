import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest

from services.core.operations.users_operations import \
    encrypt, authenticate, initializeUser, \
    userReadOperation, userCreateOperation, userUpdateOperation

from exceptions import ErrorWithCode

from models import db, User
from run_test import create_app

app = create_app()
app.app_context().push()
db.init_app(app)

class Test_users_operations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()

        u = initializeUser('john_doe@gmail.com', 'password')
        db.session.add(u)
        db.session.commit()

    def test_encryption(self):

        plaintext_password = 'random_password'
        encrypted_password = encrypt(plaintext_password)
        self.assertTrue(authenticate(plaintext_password, encrypted_password))

    def test_userReadOperation(self):

        with self.assertRaises(ErrorWithCode):
            userReadOperation('john_doe_1@gmail.com')

        self.assertIsNotNone(userReadOperation('john_doe@gmail.com'))

    def test_userCreateOperation(self):

        with self.assertRaises(ErrorWithCode):
            userCreateOperation('john_doe@gmail.com', 'password')

        self.assertIsNotNone(userCreateOperation('john_doe_2@gmail.com', 'password'))

    def test_userUpdateOperation(self):

        with self.assertRaises(ErrorWithCode):
            userUpdateOperation('john_doe_2@gmail.com', 'password', 'password_new')
            userUpdateOperation('john_doe@gmail.com', 'password_wrong', 'password_new')

        self.assertIsNotNone(userUpdateOperation('john_doe@gmail.com', 'password', 'password_new'))

if __name__ == '__main__':
    unittest.main()
    