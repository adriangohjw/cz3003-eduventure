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

from services.core.contracts.rs_student_course_enrols_contracts import \
    courseMngReadContract, courseMngCreateContract


class Test_rs_student_course_enrols_contracts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def test_courseMngReadContract(self):

        with app.test_request_context('/?user_email=joe@gmail.com', method='GET'):
            self.assertEqual(
                courseMngReadContract(request), 
                {
                    'user_email': 'joe@gmail.com'
                }
            )

        with app.test_request_context('/?user_email=joegmail.com', method='GET'):
            self.assertRaises(ValueError, courseMngReadContract, request)

        with app.test_request_context('/?user_email=', method='GET'):
            self.assertRaises(ValueError, courseMngReadContract, request)


    def test_courseMngCreateContract(self):

        with app.test_request_context('/?user_email=joe@gmail.com&course_index=cz3003', method='POST'):
            self.assertEqual(
                courseMngCreateContract(request), 
                {
                    'user_email': 'joe@gmail.com',
                    'course_index': 'cz3003' 
                }
            )

        with app.test_request_context('/?user_email=joe@gmail.com', method='POST'):
            self.assertRaises(TypeError, courseMngCreateContract, request)

        with app.test_request_context('/?user_email=joe@gmail.com&course_index=', method='POST'):
            self.assertRaises(ValueError, courseMngCreateContract, request)

        with app.test_request_context('/?user_email=joegmail.com&course_index=cz3003', method='POST'):
            self.assertRaises(ValueError, courseMngCreateContract, request)


if __name__ == '__main__':
    unittest.main()
