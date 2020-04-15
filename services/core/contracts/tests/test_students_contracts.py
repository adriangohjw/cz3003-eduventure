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

from services.core.contracts.students_contracts import \
    validate_matriculation_number, \
    studentCreateContract, studentReadContract


class Test_students_contracts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def test_validate_matriculation_number(self):

        with self.assertRaises(TypeError):
            validate_matriculation_number(None)

        with self.assertRaises(ValueError):
            validate_matriculation_number("")


    def test_studentReadContract(self):

        with app.test_request_context('/?email=joe@gmail.com', method='GET'):
            self.assertEqual(
                studentReadContract(request), 
                {
                    'email': 'joe@gmail.com'
                }
            )

        with app.test_request_context('/?email=', method='GET'):
            self.assertRaises(ValueError, studentReadContract, request)

        with app.test_request_context('/?email=joegmail.com', method='GET'):
            self.assertRaises(ValueError, studentReadContract, request)


    def test_studentCreateContract(self):

        with app.test_request_context('/?email=joe@gmail.com&password=12345&matriculation_number=u1722', method='POST'):
            self.assertEqual(
                studentCreateContract(request), 
                {
                    'email': 'joe@gmail.com',
                    'password': '12345',
                    'matriculation_number': 'u1722',
                    'name': None
                }
            )
        
        with app.test_request_context('/?email=joe@gmail.com&password=12345&matriculation_number=u1722&name=Joe', method='POST'):
            self.assertEqual(
                studentCreateContract(request), 
                {
                    'email': 'joe@gmail.com',
                    'password': '12345',
                    'matriculation_number': 'u1722',
                    'name': 'Joe'
                }
            )

        with app.test_request_context('/?email=joe@gmail.com&password=12345', method='POST'):
            self.assertRaises(TypeError, studentCreateContract, request)

        with app.test_request_context('/?email=&password=12345&matriculation_number=', method='POST'):
            self.assertRaises(ValueError, studentCreateContract, request)

        with app.test_request_context('/?email=joegmail.com&password=12345&matriculation_number=', method='POST'):
            self.assertRaises(ValueError, studentCreateContract, request)


if __name__ == '__main__':
    unittest.main()
