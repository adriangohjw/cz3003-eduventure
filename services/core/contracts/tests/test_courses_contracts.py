import sys
from os import path, getcwd
from flask import Flask
from flask import request
sys.path.append(getcwd())

import unittest

from services.core.contracts.courses_contracts import validate_index,courseCreateContract,courseReadContract
from models import db
from run_test import create_app

app = create_app()
app.app_context().push()
db.init_app(app)

class Test_courses_contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def test_validate_index(self):
        with self.assertRaises(TypeError):

            validate_index(None)

        with self.assertRaises(ValueError):
            validate_index("")

    def test_lessonDeleteContract(self):
        with app.test_request_context('/?index=12', method='POST'):
            self.assertEqual(courseReadContract(request), { 'index':'12' })

        with app.test_request_context('/?index=', method='POST'):
            # now you can do something with the request until the
            # end of the with block, such as basic assertions:
            # assert request.path == '/hello'
            with self.assertRaises(ValueError):
                courseReadContract(request)

    def test_courseCreateContract(self):
        with app.test_request_context('/?index=12', method='POST'):
            self.assertEqual(courseCreateContract(request), { 'index':'12' })

        with app.test_request_context('/?index=', method='POST'):
            # now you can do something with the request until the
            # end of the with block, such as basic assertions:
            # assert request.path == '/hello'
            with self.assertRaises(ValueError):
                 courseCreateContract(request)


if __name__ == '__main__':
    unittest.main()
