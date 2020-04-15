import sys
from os import path, getcwd
sys.path.append(getcwd())

from flask import request
import unittest

from models import db
from run_test import create_app

from test_BaseCase import Test_BaseCase, res_to_dict


class Test_topicsController(Test_BaseCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def test_TopicAPI_GET(self):

        # invalid params input
        response = self.app.get('/topics?id=')
        self.assertEqual(response.status_code, 400)

        # record not found
        response = self.app.get('/topics?id=3')
        self.assertEqual(response.status_code, 409)
        
        # success case
        response = self.app.get('/topics?id=1')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['name'], 'topic_1')


    def test_TopicAPI_POST(self):

        # invalid params input
        response = self.app.post('/topics?name=')
        self.assertEqual(response.status_code, 400)

        # existing record
        response = self.app.post('/topics?name=topic_1')
        self.assertEqual(response.status_code, 409)

         # success case
        response = self.app.post('/topics?name=topic_3')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['name'], 'topic_3')


    def test_TopicAPI_PUT(self):

        # invalid params input
        response = self.app.put('/topics?id=&name=new_name')
        self.assertEqual(response.status_code, 400)

        response = self.app.put('/topics?id=1&name=')
        self.assertEqual(response.status_code, 400)

        # record not found
        response = self.app.put('/topics?id=3&name=new_name')
        self.assertEqual(response.status_code, 409)

        # success case
        response = self.app.put('/topics?id=1&name=new_name')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['name'], 'new_name')


    def test_TopicAPI_DELETE(self):

        # invalid params input
        response = self.app.delete('/topics?id=')
        self.assertEqual(response.status_code, 400)

        # record not found
        response = self.app.delete('/topics?id=3')
        self.assertEqual(response.status_code, 409)

        # record is a dependency
        response = self.app.delete('/topics?id=2') 
        self.assertEqual(response.status_code, 409)

        # success case
        from models import Lesson 
        lessons = Lesson.query.filter_by(topic_id=2).all()
        for lesson in lessons:
            db.session.delete(lesson)
        db.session.commit()

        response = self.app.delete('/topics?id=2') 
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['message'], 'Successfully deleted topic')

        from models import Topic
        topic = Topic.query.filter_by(id=2).first() 
        self.assertIsNone(topic)


    def test_TopicListAPI_GET(self):
        
        # success case
        response = self.app.get('/topics/all')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res['topics']), 2)
        self.assertEqual(res['topics'][0]['name'], 'topic_1')
        self.assertEqual(res['topics'][1]['name'], 'topic_2')


if __name__ == '__main__':
    unittest.main()
    