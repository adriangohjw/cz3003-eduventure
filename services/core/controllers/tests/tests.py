import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest

from services.core.controllers.tests.test_UsersController import Test_usersController

if __name__ == '__main__':
    unittest.main()
