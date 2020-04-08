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

from services.core.contracts.courses_contracts import \
    validate_index, courseCreateContract, courseReadContract


class Test_courses_contracts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def test_validate_index(self):

        with self.assertRaises(TypeError):
            validate_index(None)

        with self.assertRaises(ValueError):
            validate_index("")


    def test_courseReadContract(self):

        with app.test_request_context('/?index=cz3003', method='GET'):
            self.assertEqual(
                courseReadContract(request), 
                {
                    'index': 'cz3003'
                }
            )

        with app.test_request_context('/?index=', method='GET'):
            self.assertRaises(ValueError, courseReadContract, request)


    def test_courseCreateContract(self):

        with app.test_request_context('/?index=cz3003', method='POST'):
            self.assertEqual(
                courseCreateContract(request), 
                {
                    'index': 'cz3003'
                }
            )

        with app.test_request_context('/?index=', method='POST'):
            self.assertRaises(ValueError, courseCreateContract, request)


if __name__ == '__main__':
    unittest.main()
