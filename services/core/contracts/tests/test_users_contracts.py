import sys
from os import path, getcwd
sys.path.append(path.dirname(path.dirname((getcwd()))))

print(sys.path)

import requests
import unittest

from contracts.users_contracts import validate_email, validate_password

class Test_user_contracts(unittest.TestCase):

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
        

if __name__ == '__main__':
    unittest.main()
    