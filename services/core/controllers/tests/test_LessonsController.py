
import sys
from os import path, getcwd
sys.path.append(getcwd())

from flask import request
import unittest

from models import db
from run_test import create_app

from test_BaseCase import Test_BaseCase, res_to_dict


"""
This is a TestCase object to test the functions in lessonsController.py
"""
class Test_lessonsController(Test_BaseCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # test the GET request for LessonAPI
    def test_LessonAPI_GET(self):

        # request has invalid params input
        response = self.app.get('/lessons?topic_id=1&lesson_id=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record not found
        response = self.app.get('/lessons?topic_id=3&lesson_id=1')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 409)
        
        # success case
        response = self.app.get('/lessons?topic_id=1&lesson_id=1')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['name'], 'lesson_1')

    # test the POST request for LessonAPI
    def test_LessonAPI_POST(self):

        # request has invalid params input
        response = self.app.post('/lessons?topic_id=1&name=new_lesson')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record already exist
        response = self.app.post('/lessons?topic_id=1&name=lesson_1&content=content&url_link=https%3A%2F%2Fwww.google.com')
        # check if status code is correct
        print('--- check if status code is correct (record already exist)')
        self.assertEqual(response.status_code, 409)

        # success case
        response = self.app.post('/lessons?topic_id=2&name=lesson_5&content=content')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (1), check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful (1), check if JSON returned is correct')
        self.assertEqual(res['name'], 'lesson_5')
        self.assertEqual(res['url_link'], None)

        response = self.app.post('/lessons?topic_id=2&name=lesson_6&content=content&url_link=https%3A%2F%2Fwww.google.com')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (2), check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful (2), check if JSON returned is correct')
        self.assertEqual(res['name'], 'lesson_6')
        self.assertEqual(res['url_link'], 'https://www.google.com')

    # test the PUT request for LessonAPI
    def test_LessonAPI_PUT(self):

        # request has invalid params input
        response = self.app.put('/lessons?topic_id=1&lesson_id=1&col=wrong_value&value=hello')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record not found
        response = self.app.put('/lessons?topic_id=3&lesson_id=1&col=name&value=lesson_10')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 409)

        # success case
        response = self.app.put('/lessons?topic_id=1&lesson_id=1&col=name&value=lesson_10')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (1), check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful (1), check if JSON returned is correct')
        self.assertEqual(res['name'], 'lesson_10')

        response = self.app.put('/lessons?topic_id=1&lesson_id=1&col=content&value=content_new')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (2), check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful (2), check if JSON returned is correct')
        self.assertEqual(res['content'], 'content_new')

        response = self.app.put('/lessons?topic_id=1&lesson_id=1&col=url_link&value=https%3A%2F%2Fwww.facebook.com')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (3), check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful (3), check if JSON returned is correct')
        self.assertEqual(res['url_link'], 'https://www.facebook.com')

    # test the DELETE request for LessonAPI
    def test_LessonAPI_DELETE(self):
        
        # request has invalid params input
        response = self.app.delete('/lessons?topic_id=2&lesson_id=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record not found
        response = self.app.delete('/lessons?topic_id=2&lesson_id=2')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 409)

        # success case
        response = self.app.delete('/lessons?topic_id=2&lesson_id=1')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['message'], 'Successfully deleted lesson')

    # test the GET request for LessonListAPI
    def test_LessonListAPI_GET(self):
        
        # success case
        response = self.app.get('/lessons/all')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(len(res['lessons']), 4)
        self.assertEqual(res['lessons'][0]['name'], 'lesson_1')
        self.assertEqual(res['lessons'][1]['name'], 'lesson_2')

    # test the GET request for QuizManagerAPI
    def test_lesson_QuizManagerAPI_GET(self):

        # request has invalid params input
        response = self.app.get('/lessons/quizzes?topic_id=1')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as dependency record not found
        response = self.app.get('/lessons/quizzes?topic_id=2&lesson_id=2')
        # check if status code is correct
        print('--- check if status code is correct (dependency record not found)')
        self.assertEqual(response.status_code, 409)

        # request error as record not found
        response = self.app.get('/lessons/quizzes?topic_id=1&lesson_id=2')
        res = res_to_dict(response)
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 409)

        # success case
        response = self.app.get('/lessons/quizzes?topic_id=1&lesson_id=1')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(len(res['quiz']), 2)

    # test the POST request for QuizManagerAPI
    def test_lesson_QuizManagerAPI_POST(self):

        # request has invalid params input
        response = self.app.post('/lessons/quizzes?topic_id=1')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as dependency record not found
        response = self.app.post('/lessons/quizzes?topic_id=2&lesson_id=2&quiz_id=1')
        # check if status code is correct
        print('--- check if status code is correct (dependency record not found)')
        self.assertEqual(response.status_code, 409)

        # request error as record already exist
        response = self.app.post('/lessons/quizzes?topic_id=1&lesson_id=1&quiz_id=1')
        # check if status code is correct
        print('--- check if status code is correct (record already exist)')
        self.assertEqual(response.status_code, 409)
        db.session.rollback()

        # success case 
        response = self.app.post('/lessons/quizzes?topic_id=2&lesson_id=1&quiz_id=1')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['topic_id'], 2)
        self.assertEqual(res['lesson_id'], 1)
        self.assertEqual(res['quiz_id'], 1)

    # test the DELETE request for QuizManagerAPI
    def test_lesson_QuizManagerAPI_DELETE(self):

        # request has invalid params input
        response = self.app.delete('/lessons/quizzes?id=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record not found
        response = self.app.delete('/lessons/quizzes?id=4')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 409)

        # success case
        response = self.app.delete('/lessons/quizzes?id=1')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['message'], 'Successfully deleted rs')


if __name__ == '__main__':
    unittest.main(verbosity=2)
    