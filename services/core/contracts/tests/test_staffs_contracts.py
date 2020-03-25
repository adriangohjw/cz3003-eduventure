import sys
from os import path, getcwd

sys.path.append(getcwd())
from flask import Flask
from flask import request
import unittest

from services.core.contracts.staffs_contracts import staffCreateContract,staffReadContract
from models import db
from run_test import create_app

app = create_app()
app.app_context().push()
db.init_app(app)

class Test_staffs_contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def test_staffReadContract(self):
        with app.test_request_context('/?email=joe@gmail.com', method='POST'):
            self.assertEqual(staffReadContract(request), {'email':'joe@gmail.com'})
        # test not passed as it throws a TypeError since duration_ms is not integer in validate_duration_ms()

        with app.test_request_context('/?email=joegmail.com', method='POST'):
            # now you can do something with the request until the
            # end of the with block, such as basic assertions:
            # assert request.path == '/hello'
            with self.assertRaises(ValueError):
                staffReadContract(request)

    def test_staffCreateContract(self):
        with app.test_request_context('/?email=joe@gmail.com&password=12345', method='POST'):
            self.assertEqual(staffCreateContract(request), {'email':'joe@gmail.com',
        'password': '12345'})

        with app.test_request_context('/?email=joegmail.com&password=12345', method='POST'):
            # now you can do something with the request until the
            # end of the with block, such as basic assertions:
            # assert request.path == '/hello'
            with self.assertRaises(ValueError):
                staffCreateContract(request)

if __name__ == '__main__':
    unittest.main()
