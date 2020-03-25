import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from services.core.operations.courses_operations import initializeCourse,courseCreateOperation,courseReadOperation

from exceptions import ErrorWithCode

from models import db, User
from run_test import create_app

app = create_app()
app.app_context().push()
db.init_app(app)


class Test_courses_operations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()

        c = initializeCourse('cz3003')
        db.session.add(c)
        db.session.commit()

    def test_courseReadOperation(self):
        with self.assertRaises(ErrorWithCode):
            courseReadOperation('cz3007')

        self.assertIsNotNone(courseReadOperation('cz3003'))

    def test_courseCreateOperation(self):
        with self.assertRaises(ErrorWithCode):
            courseCreateOperation('cz3003')
            courseCreateOperation('')

        self.assertIsNotNone(courseCreateOperation('cz3007'))


if __name__ == '__main__':
    unittest.main()
