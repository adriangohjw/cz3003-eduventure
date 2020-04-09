import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from services.core.operations.staffs_operations import staffCreateOperation, staffReadOperation,initializeStaff

from exceptions import ErrorWithCode

from models import db
from run_test import create_app

app = create_app()
app.app_context().push()
db.init_app(app)


class Test_staffs_operations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()

        sf = initializeStaff('john_doe@gmail.com', 'password', 'John Doe')
        db.session.add(sf)
        db.session.commit()

    def test_staffReadOperation(self):
        with self.assertRaises(ErrorWithCode):
            staffReadOperation('john_doe_1@gmail.com')

        self.assertIsNotNone(staffReadOperation('john_doe@gmail.com'))

    def test_staffCreateOperation(self):
        with self.assertRaises(ErrorWithCode):
            staffCreateOperation('john_doe@gmail.com', 'password', 'John Doe')

        self.assertIsNotNone(staffCreateOperation('john_doe_2@gmail.com', 'password', 'John Doe Tan'))

        self.assertEqual(
            staffCreateOperation('john_doe_3@gmail.com', 'password', 'John Doe Goh').name,
            'John Doe Goh'
        )

if __name__ == '__main__':
    unittest.main()
