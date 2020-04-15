import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest

from models import db,Topic
from run_test import create_app
app = create_app()
app.app_context().push()
db.init_app(app)

from services.core.operations.users_operations import encrypt
from services.core.dao.TopicsDAO import \
    topicCreate, topicRead, topicUpdate, topicDelete, topiclistRead


class Test_TopicsDAO(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()


    def test_topicCreate(self):

        top = Topic(name="architecture")
        topicCreate(top)

        top_list = Topic.query.all()

        self.assertEqual(1, len(top_list))
        self.assertEqual(top_list[0].name, "architecture")


    def test_topicRead(self):

        top = Topic(name="architecture")

        db.session.add(top)
        db.session.commit()

        top_list = Topic.query.all()

        self.assertTrue(topicRead('name','architecture'))
        self.assertTrue(topicRead('id',1))

    def test_topicUpdate(self):

        top = Topic(name="architecture")

        db.session.add(top)
        db.session.commit()

        top.name = 'srs'
        topicUpdate()

        top = Topic.query.filter_by(id=1).first()
        self.assertEqual('srs', top.name)


    def test_topicDelete(self):

        topic = Topic(name="architecture")
        db.session.add(topic)
        db.session.commit()

        self.assertEqual(len(Topic.query.all()), 1)

        topicDelete(1)

        self.assertEqual(len(Topic.query.all()), 0)


    def test_topiclistRead(self):

        self.assertEqual(len(topiclistRead()), 0)
        
        self.assertEqual(
            topiclistRead(), []
        )

        topic_1 = Topic('topic_1')
        db.session.add(topic_1)
        db.session.commit()

        self.assertEqual(len(topiclistRead()), 1)     

        self.assertEqual(topiclistRead()[0].name, 'topic_1')   


if __name__ == '__main__':
    unittest.main()
