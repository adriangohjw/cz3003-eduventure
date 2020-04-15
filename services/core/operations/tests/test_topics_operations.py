import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from exceptions import ErrorWithCode

from models import db
from run_test import create_app
app = create_app()
app.app_context().push()
db.init_app(app)

from services.core.operations.topics_operations import \
    initializeTopic,topicCreateOperation,topicReadOperation, topicUpdateOperation, topicDeleteOperation, \
    topiclistReadOperation
from services.core.operations.lessons_operations import \
    initializeLesson
from models import Topic


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


    def test_topicUpdateOperation(self):

        with self.assertRaises(ErrorWithCode):
            topicUpdateOperation(0, 'new_name')
            topicCreateOperation(1, '')

        self.assertTrue(topicUpdateOperation(1, 'new_name').name, 'new_name')


    def test_topicDeleteOperation(self):

        self.assertEqual(len(Topic.query.all()), 1)

        lesson = initializeLesson(1, 'lesson_1', 'content_1', None)
        db.session.add(lesson)
        db.session.commit()

        self.assertRaises(ErrorWithCode, topicDeleteOperation, 1)
        self.assertEqual(len(Topic.query.all()), 1)

        db.session.delete(lesson)
        db.session.commit()
        
        self.assertTrue(topicDeleteOperation(1))
        self.assertEqual(len(Topic.query.all()), 0)


    def test_topiclistReadOperation(self):

        self.assertEqual(len(topiclistReadOperation()), 1)
        
        self.assertEqual(topiclistReadOperation()[0].name, 'srs')


if __name__ == '__main__':
    unittest.main()
