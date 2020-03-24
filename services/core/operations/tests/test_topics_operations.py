import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from services.core.operations.topics_operations import initializeTopic,topicCreateOperation,topicReadOperation

from exceptions import ErrorWithCode

from models import db
from run_test import create_app

app = create_app()
app.app_context().push()
db.init_app(app)


class Test_topics_operations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()

        sf = initializeTopic('srs')
        db.session.add(sf)
        db.session.commit()

    def test_topicReadOperation(self):
        with self.assertRaises(ErrorWithCode):
            topicReadOperation(2)

        self.assertIsNotNone(topicReadOperation(1))

    def test_topicCreateOperation(self):
        with self.assertRaises(ErrorWithCode):
            topicCreateOperation('srs')
            topicCreateOperation('')

        self.assertIsNotNone(topicCreateOperation('patterns'))

if __name__ == '__main__':
    unittest.main()
