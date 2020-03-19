import sys
from os import path, getcwd

sys.path.append(getcwd())

import requests
import unittest

from services.core.contracts.users_contracts import validate_email, validate_password

class Test_user_contracts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def setUp(self):
        print("\n>>>>> {}: starting test...".format(self._testMethodName))

    def tearDown(self):
        print(">>>>> {}: ending test...".format(self._testMethodName))

    def test_validate_email(self):

        with self.assertRaises(TypeError):

            validate_email(None)

        with self.assertRaises(ValueError):

            validate_email("")
            
            validate_email("@gmail.com")
            validate_email("johndoegmail.com")
            validate_email("johndoe@gmailcom")
            
    def test_validate_password(self):

        with self.assertRaises(TypeError):

            validate_password(None)

        with self.assertRaises(ValueError):

            validate_password("")

    @classmethod
    def tearDownClass(cls):
        print("\n{}: ending test...".format(path.basename(__file__)))

if __name__ == '__main__':
    unittest.main()
    