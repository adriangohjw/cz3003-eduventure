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

import datetime
from services.quiz.contracts.quizzes_contracts import \
    validate_id, validate_name, validate_date_end, validate_date_start, validate_is_fast, validate_staff_id, \
    quizCreateContract, quizDeleteContract, quizReadContract, quizUpdateContract


class Test_quizzes_contracts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def test_validate_id(self):

        with self.assertRaises(TypeError):
            validate_id(None)
            validate_id("")


    def test_validate_staff_id(self):

        with self.assertRaises(TypeError):
            validate_staff_id(None)
        
        with self.assertRaises(ValueError):
            validate_staff_id("")


    def test_validate_name(self):

        with self.assertRaises(TypeError):
            validate_name(None)

        with self.assertRaises(ValueError):
            validate_name("")


    def test_validate_is_fast(self):

        with self.assertRaises(TypeError):
            validate_is_fast(None)
            validate_is_fast(1)
            validate_is_fast(1.1)
            validate_is_fast("")


    def test_validate_date_start(self):

        with self.assertRaises(TypeError):
            validate_date_start(None)

        with self.assertRaises(ValueError):
            validate_date_start("")
            validate_date_start("20-4-5")


    def test_validate_date_end(self):
        
        with self.assertRaises(TypeError):
            validate_date_end(None)
        
        with self.assertRaises(ValueError):
            validate_date_end("")
            validate_date_end("20-4-5")


    def test_quizReadContract(self):

        with app.test_request_context('/?id=2', method='GET'):
            self.assertEqual(
                quizReadContract(request), 
                {
                    'id': 2 
                }
            )

        with app.test_request_context('/?id=', method='GET'):
            self.assertRaises(TypeError, quizReadContract, request)


    def test_quizCreateContract(self):

        with app.test_request_context('/?staff_id=20&name=Joe&is_fast=true&date_start=2020-03-24&date_end=2020-03-25', method='POST'):
            self.assertEqual(
                quizCreateContract(request), 
                {
                    'staff_id': 20,
                    'name': 'Joe',
                    'is_fast': True,
                    'date_start': datetime.date(2020, 3, 24),
                    'date_end': datetime.date(2020, 3, 25)
                }
            )

        with app.test_request_context('/?staff_id=20&name=Joe&is_fast=true&date_start=2020-03-24&date_end=2020:03:25', method='POST'):
            self.assertRaises(ValueError, quizCreateContract, request)

        with app.test_request_context('/?staff_id=20&name=Joe&is_fast=true&date_start=2020-03-24&date_end=', method='POST'):
            self.assertRaises(ValueError, quizCreateContract, request)


    def test_quizUpdateContract(self):

        with app.test_request_context('/?id=3&name=Joe&is_fast=true&date_start=2020-03-24&date_end=2020-03-25', method='PUT'):
            self.assertEqual(
                quizUpdateContract(request),
                {
                    'id': 3,
                    'name': 'Joe',
                    'is_fast': True,
                    'date_start': datetime.date(2020, 3, 24),
                    'date_end': datetime.date(2020, 3, 25)
                }
            )

        with app.test_request_context('/?id=3', method='PUT'):
            self.assertRaises(TypeError, quizUpdateContract, request)

        with app.test_request_context('/?id=3&name=&is_fast=true&date_start=2020-03-24&date_end=2020-03-25', method='PUT'):
            self.assertRaises(ValueError, quizUpdateContract, request)

        with app.test_request_context('/?id=3&name=Joe&is_fast=true&date_start=2020-03-24&date_end=20200325', method='PUT'):
            self.assertRaises(ValueError, quizUpdateContract, request)


    def test_quizDeleteContract(self):

        with app.test_request_context('/?id=2', method='DELETE'):
            self.assertEqual(
                quizDeleteContract(request), 
                {
                    'id': 2 
                }
            )

        with app.test_request_context('/?id=', method='DELETE'):
            self.assertRaises(TypeError, quizDeleteContract, request)


if __name__ == '__main__':
    unittest.main()
