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

from services.core.contracts.staffs_contracts import \
    validate_name, staffCreateContract, staffReadContract


class Test_staffs_contracts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def test_validate_name(self):

        with self.assertRaises(TypeError):
            validate_name(None)

        with self.assertRaises(ValueError):
            validate_name("")


    def test_staffReadContract(self):

        with app.test_request_context('/?email=joe@gmail.com', method='GET'):
            self.assertEqual(
                staffReadContract(request), 
                {
                    'email': 'joe@gmail.com'
                }
            )

        with app.test_request_context('/?email=joegmail.com', method='GET'):
            self.assertRaises(ValueError, staffReadContract, request)

        with app.test_request_context('/?email=', method='GET'):
            self.assertRaises(ValueError, staffReadContract, request)


    def test_staffCreateContract(self):
        with app.test_request_context('/?email=joe@gmail.com&password=12345&name=John%20Doe', method='POST'):
            self.assertEqual(
                staffCreateContract(request), 
                {
                    'email': 'joe@gmail.com',
                    'password': '12345',
                    'name': 'John Doe'
                }
            )

        with app.test_request_context('/?email=joegmail.com', method='POST'):
            self.assertRaises(ValueError, staffCreateContract, request)

        with app.test_request_context('/?email=', method='POST'):
            self.assertRaises(ValueError, staffCreateContract, request)

        with app.test_request_context('/?email=joegmail.com&password=12345', method='POST'):
            self.assertRaises(ValueError, staffCreateContract, request)


if __name__ == '__main__':
    unittest.main()
