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

from services.core.contracts.statistics_contracts import \
    studentScoreReadContract


class Test_statistics_contracts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def test_studentScoreReadContract(self):

        with app.test_request_context('/?student_id=1', method='GET'):
            self.assertEqual(
                studentScoreReadContract(request), 
                {
                    'student_id': 1
                }
            )


if __name__ == '__main__':
    unittest.main()
