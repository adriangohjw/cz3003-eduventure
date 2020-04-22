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

from services.quiz.contracts.quizzes_contracts import (
    validate_id, 
    validate_name, 
    validate_date_end, 
    validate_date_start, 
    validate_is_fast, 
    validate_staff_id, 
    quizCreateContract, 
    quizDeleteContract, 
    quizReadContract, 
    quizUpdateContract
)
    

"""
This is a TestCase object to test the functions in quizzes_contracts.py
"""
class Test_quizzes_contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # test the function validate_id
    def test_validate_id(self):
        print('\r')

        # check if TypeError raised when arg is None type
        print('--- test if arg is None type')
        self.assertRaises(TypeError, validate_id, None)

        # check if TypeError raised when arg is string type
        print('--- test if arg is string type')
        self.assertRaises(TypeError, validate_id, 'testing')

        # check if TypeError raised when arg is float type
        print('--- test if arg is float type')
        self.assertRaises(TypeError, validate_id, 1.1)

        # check if TypeError raised when arg is boolean type
        print('--- test if arg is boolean type')
        self.assertRaises(TypeError, validate_id, True)

    # test the function validate_staff_id
    def test_validate_staff_id(self):
        print('\r')

        # check if TypeError raised when arg is None type
        print('--- test if arg is None type')
        self.assertRaises(TypeError, validate_staff_id, None)

        # check if TypeError raised when arg is string type
        print('--- test if arg is string type')
        self.assertRaises(TypeError, validate_staff_id, 'testing')

        # check if TypeError raised when arg is float type
        print('--- test if arg is float type')
        self.assertRaises(TypeError, validate_staff_id, 1.1)

        # check if TypeError raised when arg is boolean type
        print('--- test if arg is boolean type')
        self.assertRaises(TypeError, validate_staff_id, True)

    # test the function validate_name
    def test_validate_name(self):
        print('\r')

        # check if TypeError raised when arg is None type
        print('--- test if arg is None type')
        self.assertRaises(TypeError, validate_name, None)

        # check if ValueError raised when arg is empty string
        print('--- test if arg is empty string')
        self.assertRaises(ValueError, validate_name, '')

    # test the function validate_is_fast
    def test_validate_is_fast(self):
        print('\r')

        # check if TypeError raised when arg is None type
        print('--- test if arg is None type')
        self.assertRaises(TypeError, validate_is_fast, None)

        # check if TypeError raised when arg is string type
        print('--- test if arg is string type')
        self.assertRaises(TypeError, validate_is_fast, 'testing')

        # check if TypeError raised when arg is integer type
        print('--- test if arg is float type')
        self.assertRaises(TypeError, validate_is_fast, 1)

        # check if TypeError raised when arg is float type
        print('--- test if arg is float type')
        self.assertRaises(TypeError, validate_is_fast, 1.1)

    # test the function validate_date_start
    def test_validate_date_start(self):
        print('\r')

        # check if TypeError raised when arg is None type
        print('--- test if arg is None type')
        self.assertRaises(TypeError, validate_date_start, None)

        # check if ValueError raised when arg is empty string
        print('--- test if arg is empty string')
        self.assertRaises(ValueError, validate_date_start, '')

        # check if ValueError raised when arg is in the wrong format
        print('--- test if arg is in the wrong format')
        self.assertRaises(ValueError, validate_date_start, '20-4-5')

    # test the function validate_date_end
    def test_validate_date_end(self):
        print('\r')
        
        # check if TypeError raised when arg is None type
        print('--- test if arg is None type')
        self.assertRaises(TypeError, validate_date_end, None)

        # check if ValueError raised when arg is empty string
        print('--- test if arg is empty string')
        self.assertRaises(ValueError, validate_date_end, '')

        # check if ValueError raised when arg is in the wrong format
        print('--- test if arg is in the wrong format')
        self.assertRaises(ValueError, validate_date_end, '20-4-5')

    # test the function quizReadContract
    def test_quizReadContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?id=2', method='GET'):
            # check res returned by func is correct
            self.assertEqual(
                quizReadContract(request), 
                {
                    'id': 2 
                }
            )

        # passing request with unacceptable value in params (no value passed into 'id')
        print('--- test request with unacceptable params value (no value for \'id\')')
        with app.test_request_context('/?id=', method='GET'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, quizReadContract, request)

    # test the function quizCreateContract
    def test_quizCreateContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?staff_id=20&name=Joe&is_fast=true&date_start=2020-03-24&date_end=2020-03-25', method='POST'):
            # check res returned by func is correct
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

        # passing request with unacceptable value in params (wrong format passed into 'date_end')
        print('--- test request with unacceptable params value (wrong format for \'date_end\')')
        with app.test_request_context('/?staff_id=20&name=Joe&is_fast=true&date_start=2020-03-24&date_end=2020:03:25', method='POST'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, quizCreateContract, request)

        # passing request with unacceptable value in params (no value passed into 'date_end')
        print('--- test request with unacceptable params value (no value for \'date_end\')')
        with app.test_request_context('/?staff_id=20&name=Joe&is_fast=true&date_start=2020-03-24&date_end=', method='POST'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, quizCreateContract, request)

    # test the function quizUpdateContract
    def test_quizUpdateContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?id=3&name=Joe&is_fast=true&date_start=2020-03-24&date_end=2020-03-25', method='PUT'):
            # check res returned by func is correct
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

        # passing request with missing params (params missing)
        print('--- test request with missing params')
        with app.test_request_context('/?id=3', method='PUT'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, quizUpdateContract, request)

        # passing request with unacceptable value in params (no value passed into 'name')
        print('--- test request with unacceptable params value (no value for \'name\')')
        with app.test_request_context('/?id=3&name=&is_fast=true&date_start=2020-03-24&date_end=2020-03-25', method='PUT'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, quizUpdateContract, request)

        # passing request with unacceptable value in params (no value passed into 'date_end')
        print('--- test request with unacceptable params value (no value for \'date_end\')')
        with app.test_request_context('/?id=3&name=Joe&is_fast=true&date_start=2020-03-24&date_end=20200325', method='PUT'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, quizUpdateContract, request)

    # test the function quizDeleteContract
    def test_quizDeleteContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?id=2', method='DELETE'):
            # check res returned by func is correct
            self.assertEqual(
                quizDeleteContract(request), 
                {
                    'id': 2 
                }
            )

        # passing request with unacceptable value in params (no value passed into 'id')
        print('--- test request with unacceptable params value (no value for \'id\')')
        with app.test_request_context('/?id=', method='DELETE'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, quizDeleteContract, request)


if __name__ == '__main__':
    unittest.main(verbosity=2)
