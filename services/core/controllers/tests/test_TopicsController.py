import sys
from os import path, getcwd
sys.path.append(getcwd())

from flask import request
import unittest

from models import db, Topic, Lesson
from run_test import create_app

from test_BaseCase import Test_BaseCase, res_to_dict


"""
This is a TestCase object to test the functions in topicsController.py
"""
class Test_topicsController(Test_BaseCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # test the GET request for TopicAPI
    def test_TopicAPI_GET(self):

        # request has invalid params input
        response = self.app.get('/topics?id=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record not found
        response = self.app.get('/topics?id=3')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 409)
        
        # success case
        response = self.app.get('/topics?id=1')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['name'], 'topic_1')

    # test the POST request for TopicAPI
    def test_TopicAPI_POST(self):

        # request has invalid params input
        response = self.app.post('/topics?name=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record already exist
        response = self.app.post('/topics?name=topic_1')
        # check if status code is correct
        print('--- check if status code is correct (record already exist)')
        self.assertEqual(response.status_code, 409)

        # success case
        response = self.app.post('/topics?name=topic_3')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['name'], 'topic_3')

    # test the PUT request for TopicAPI
    def test_TopicAPI_PUT(self):

        # request has invalid params input (id is empty)
        response = self.app.put('/topics?id=&name=new_name')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input - empty id)')
        self.assertEqual(response.status_code, 400)

        # request has invalid params input (name is empty)
        response = self.app.put('/topics?id=1&name=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input - empty name)')
        self.assertEqual(response.status_code, 400)

        # request error as record not found
        response = self.app.put('/topics?id=3&name=new_name')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 409)

        # success case
        response = self.app.put('/topics?id=1&name=new_name')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['name'], 'new_name')

    # test the DELETE request for TopicAPI
    def test_TopicAPI_DELETE(self):

        # request has invalid params input
        response = self.app.delete('/topics?id=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record not found
        response = self.app.delete('/topics?id=3')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 409)

        # request error as record is a dependency
        response = self.app.delete('/topics?id=2') 
        # check if status code is correct
        print('--- check if status code is correct (record is a dependency)')
        self.assertEqual(response.status_code, 409)

        # removing dependencies rom record
        lessons = Lesson.query.filter_by(topic_id=2).all()
        for lesson in lessons:
            db.session.delete(lesson)
        db.session.commit()

        #success case
        response = self.app.delete('/topics?id=2') 
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['message'], 'Successfully deleted topic')

    # test the GET request for TopicListAPI
    def test_TopicListAPI_GET(self):
        
        # success case
        response = self.app.get('/topics/all')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(len(res['topics']), 2)
        self.assertEqual(res['topics'][0]['name'], 'topic_1')
        self.assertEqual(res['topics'][1]['name'], 'topic_2')


if __name__ == '__main__':
    unittest.main(verbosity=2)
    