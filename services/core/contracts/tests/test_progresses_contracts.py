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

from services.core.contracts.progresses_contracts import \
    validate_student_id, progressReadContract


class Test_progresses_contracts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def test_validate_student_id(self):

        with self.assertRaises(TypeError):
            validate_student_id(None)
            validate_student_id(1.1)
            validate_student_id(True)
            validate_student_id("")

    
    def test_progressReadContract(self):

        with app.test_request_context('/?student_id=1', method='GET'):
            self.assertEqual(
                progressReadContract(request), 
                {
                    'student_id': 1
                }
            )

        with app.test_request_context('/?student_id=hello', method='GET'):
            self.assertRaises(TypeError, progressReadContract, request)

        with app.test_request_context('/?student_id=', method='GET'):
            self.assertRaises(TypeError, progressReadContract, request)


if __name__ == '__main__':
    unittest.main()
