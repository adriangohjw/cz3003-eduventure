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
from services.core.dao.TopicsDAO import (
    topicCreate, 
    topicRead, 
    topicUpdate, 
    topicDelete, 
    topiclistRead
)
    

"""
This is a TestCase object to test the functions in TopicsDAO.py
"""
class Test_TopicsDAO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # this will run before every test
    # it will ensure that every test start with a fresh database
    def setUp(self):
        print('\r')
        # drop all tables in the database
        db.session.remove()
        db.drop_all()
        # crete all tables in the database
        db.create_all()

    # test the function topicCreate
    def test_topicCreate(self):

        # create a new Topic object
        top = Topic(name="architecture")

        # add Topic object to the database
        topicCreate(top)

        # retrieve all records from the table 'topics'
        top_list = Topic.query.all()

        # check that the number of record added is correct
        print('--- check that the number of record added is correct')
        self.assertEqual(1, len(top_list))

        # check that the value(s) of the Topic object added is correct
        print('--- check that the value(s) of the Topic object added is correct')
        self.assertEqual(top_list[0].name, "architecture")

    # test the function topicRead
    def test_topicRead(self):

        # create a new Topic object and add it to the database
        top = Topic(name="architecture")
        db.session.add(top)
        db.session.commit()

        # check that the record retrieved is correct (using col='name')
        print('--- check that the record retrieved is correct (using col=\'name\')')
        self.assertTrue(topicRead('name','architecture'))

        # check that the record retrieved is correct (using col='id')
        print('--- check that the record retrieved is correct (using col=\'id\')')
        self.assertTrue(topicRead('id',1))

    # test the function topicUpdate
    def test_topicUpdate(self):

        # create a new Topic object and add it to the database
        top = Topic(name="architecture")
        db.session.add(top)
        db.session.commit()

        # update value of Topic object
        top.name = 'srs'
        topicUpdate()

        # fetch updated User object from the database
        top = Topic.query.filter_by(id=1).first()

        # check if value of Topic object has been updated
        print('--- check if value of Topic object has been updated')
        self.assertEqual('srs', top.name)

    # test the function topicDelete
    def test_topicDelete(self):

        # create a new Topic object and add it to the database
        topic = Topic(name="architecture")
        db.session.add(topic)
        db.session.commit()

        # check that record has been deleted (number of record in database -1)
        print('--- check that record has been deleted (-1 number of record in database)')
        self.assertEqual(len(Topic.query.all()), 1)
        topicDelete(1)
        self.assertEqual(len(Topic.query.all()), 0)

    # test the function topiclistRead
    def test_topiclistRead(self):

        # check that function returns the right result (when number of record = 0)
        print('--- check that function returns the right result (when number of record = 0)')
        self.assertEqual(len(topiclistRead()), 0)
        self.assertEqual(
            topiclistRead(), []
        )

        # create a new Topic object and add it to the database
        topic_1 = Topic('topic_1')
        db.session.add(topic_1)
        db.session.commit()

        # check that function returns the right result (when number of record = 1)
        print('--- check that function returns the right result (when number of record = 1)')
        self.assertEqual(len(topiclistRead()), 1)     
        self.assertEqual(topiclistRead()[0].name, 'topic_1')   


if __name__ == '__main__':
    unittest.main(verbosity=2)
