import sys
from os import path, getcwd
from flask import request
from flask import Flask

sys.path.append(getcwd())

import unittest

from services.quiz.contracts.quizzes_contracts import *


class Test_quizzes_contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def test_validate_id(self):
        with self.assertRaises(Exception):
            validate_id(None)
            validate_id("")

    def test_validate_col(self):
        with self.assertRaises(Exception):
            validate_col(None)
            validate_col("")
            validate_col("duration")

    def test_validate_staff_id(self):
        with self.assertRaises(Exception):
            validate_staff_id(None)
            validate_staff_id("")

    def test_validate_name(self):
        with self.assertRaises(Exception):
            validate_name(None)
            validate_name("")

    def test_validate_is_fast(self):
        with self.assertRaises(Exception):
            validate_is_fast(None)
            validate_is_fast("")
            validate_is_fast("notBoolean")

    def test_validate_date_start(self):
        with self.assertRaises(Exception):
            validate_date_start(None)
            validate_date_start("")
            validate_date_start("20-4-5")

    def test_validate_date_end(self):
        with self.assertRaises(Exception):
            validate_date_end(None)
            validate_date_end("")
            validate_date_end("20-4-5")

    def test_quizReadContract(self):
        app = Flask(__name__)
        with app.test_request_context('/?id=2', method='POST'):
            self.assertEqual(quizReadContract(request), { 'id': '2' })

        with app.test_request_context('/?id=', method='POST'):
            with self.assertRaises(Exception):
                quizReadContract(request)

    def test_quizCreateContract(self):
        app = Flask(__name__)
        with app.test_request_context('/?staff_id=20&name=Joe&is_fast=True&date_start=2020-03-24&date_end=2020-03-25', method='POST'):
            self.assertEqual(quizCreateContract(request), { 'staff_id': '20',
        'name': 'Joe',
        'is_fast': 'True',
        'date_start': '2020-03-24',
        'date_end': '2020-03-25' })

        with app.test_request_context('/?staff_id=20&name=Joe&is_fast=True&date_start=2020-03-24&date_end=2020:03:25', method='POST'):
            with self.assertRaises(Exception):
                quizCreateContract(request)
        with app.test_request_context('/?staff_id=20&name=Joe&is_fast=True&date_start=2020-03-24&date_end=', method='POST'):
            with self.assertRaises(Exception):
                quizCreateContract(request)

    def test_quizUpdateContract(self):
        app = Flask(__name__)
        with app.test_request_context('/?id=3&col=name&value=Joe', method='POST'):
            self.assertEqual(quizUpdateContract(request), { 'id': '3',
        'col':'name',
        'value':'Joe'})

        with app.test_request_context('/?id=3&col=name&value=', method='POST'):
            with self.assertRaises(Exception):
                quizUpdateContract(request)

        with app.test_request_context('/?id=3&col=notValid&value=Joe', method='POST'):
            with self.assertRaises(Exception):
                quizUpdateContract(request)

    def test_quizDeleteContract(self):
        app = Flask(__name__)
        with app.test_request_context('/?id=2', method='POST'):
            self.assertEqual(quizDeleteContract(request), { 'id': '2' })

        with app.test_request_context('/?id=', method='POST'):
            with self.assertRaises(Exception):
                quizDeleteContract(request)