import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from services.core.contracts.courses_contracts import *


class Test_courses_contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def test_validate_index(self):
        with self.assertRaises(TypeError):

            validate_index(None)

        with self.assertRaises(ValueError):
            validate_index("")



if __name__ == '__main__':
    unittest.main()
