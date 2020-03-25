import sys
from os import path, getcwd
from flask import request
from flask import Flask

sys.path.append(getcwd())

import unittest

from services.core.contracts.users_contracts import validate_email,validate_password,userReadContract,userCreateContract,userUpdateContract
from models import db
from run_test import create_app

app = create_app()
app.app_context().push()
db.init_app(app)
class Test_user_contracts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def test_validate_email(self):

        with self.assertRaises(TypeError):

            validate_email(None)

        with self.assertRaises(ValueError):

            validate_email("")
            
            validate_email("@gmail.com")
            validate_email("johndoegmail.com")
            validate_email("johndoe@gmailcom")
            
    def test_validate_password(self):

        with self.assertRaises(TypeError):

            validate_password(None)

        with self.assertRaises(ValueError):

            validate_password("")

    def test_userReadContract(self):
        with app.test_request_context('/?email=john_doe@gmail.com', method='POST'):
            self.assertEqual(userReadContract(request), {'email':"john_doe@gmail.com" })

        with app.test_request_context('/?email=johndoegmail.com', method='POST'):
            # now you can do something with the request until the
            # end of the with block, such as basic assertions:
            # assert request.path == '/hello'
            with self.assertRaises(ValueError):
                userReadContract(request)

        with app.test_request_context('/?email=', method='POST'):
            # now you can do something with the request until the
            # end of the with block, such as basic assertions:
            # assert request.path == '/hello'
            with self.assertRaises(ValueError):
                userReadContract(request)

        with app.test_request_context('/?email=johndoe@gmailcom', method='POST'):
            # now you can do something with the request until the
            # end of the with block, such as basic assertions:
            # assert request.path == '/hello'
            with self.assertRaises(ValueError):
                userReadContract(request)

    def test_userCreateContract(self):
        with app.test_request_context('/?email=john_doe@gmail.com&password=12345', method='POST'):
            self.assertEqual(userCreateContract(request), {'email':"john_doe@gmail.com", 'password':"12345" })

        with app.test_request_context('/?email=john_doe@gmail.com&password=', method='POST'):
            # now you can do something with the request until the
            # end of the with block, such as basic assertions:
            # assert request.path == '/hello'
            with self.assertRaises(ValueError):
                userCreateContract(request)

    def test_userUpdateContract(self):
        with app.test_request_context('/?email=john_doe@gmail.com&old_password=12345&new_password=abcde', method='POST'):
            self.assertEqual(userUpdateContract(request), {'email':"john_doe@gmail.com", 'old_password':"12345",'new_password':'abcde'  })

        with app.test_request_context('/?email=john_doe@gmail.com&old_password=12345&new_password=', method='POST'):
            # now you can do something with the request until the
            # end of the with block, such as basic assertions:
            # assert request.path == '/hello'
            with self.assertRaises(ValueError):
                userUpdateContract(request)


if __name__ == '__main__':
    unittest.main()
    