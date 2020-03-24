import sys
from os import path, getcwd
from flask import Flask
from flask import request
sys.path.append(getcwd())

import unittest

from services.core.contracts.rs_staff_course_teaches_contracts import courseMngCreateContract,courseMngReadContract


class Test_rs_staff_course_teaches_contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def test_courseMngReadContract(self):
        app = Flask(__name__)
        with app.test_request_context('/?user_email=joe@gmail.com', method='POST'):
            self.assertEqual(courseMngReadContract(request), {'user_email': 'joe@gmail.com'})

        with app.test_request_context('/?user_email=joegmail.com', method='POST'):
            with self.assertRaises(ValueError):
                courseMngReadContract(request)

        with app.test_request_context('/?user_email=', method='POST'):
            with self.assertRaises(ValueError):
                courseMngReadContract(request)

    def test_courseMngCreateContract(self):
        app = Flask(__name__)
        with app.test_request_context('/?user_email=joe@gmail.com&course_index=cz3003', method='POST'):
            self.assertEqual(courseMngCreateContract(request), {'user_email': 'joe@gmail.com','course_index':'cz3003' })

        with app.test_request_context('/?user_email=joe@gmail.com&course_index=', method='POST'):
            with self.assertRaises(ValueError):
                courseMngCreateContract(request)

        with app.test_request_context('/?user_email=joegmail.com&course_index=cz3003', method='POST'):
            with self.assertRaises(ValueError):
                courseMngCreateContract(request)

if __name__ == '__main__':
    unittest.main()