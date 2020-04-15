import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from services.core.operations.students_operations import initializeStudent, studentCreateOperation, studentReadOperation

from exceptions import ErrorWithCode

from models import db
from run_test import create_app

app = create_app()
app.app_context().push()
db.init_app(app)


class Test_students_operations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()

        sf = initializeStudent('john_doe@gmail.com', 'password','U1722', 'John Doe')
        db.session.add(sf)
        db.session.commit()

    def test_studentReadOperation(self):
        with self.assertRaises(ErrorWithCode):
            studentReadOperation('john_doe_1@gmail.com')

        self.assertIsNotNone(studentReadOperation('john_doe@gmail.com'))

    def test_studentCreateOperation(self):
        with self.assertRaises(ErrorWithCode):
            studentCreateOperation('john_doe@gmail.com', 'password','U1721', None)

        self.assertIsNotNone(studentCreateOperation('john_doe_2@gmail.com', 'password','U1721', None))
        self.assertIsNotNone(studentCreateOperation('john_doe_3@gmail.com', 'password','U1723', 'John Doe'))

if __name__ == '__main__':
    unittest.main()
