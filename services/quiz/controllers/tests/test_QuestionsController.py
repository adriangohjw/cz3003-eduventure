import sys
from os import path, getcwd
sys.path.append(getcwd())

from flask import request
import unittest

from models import db
from run_test import create_app

from test_BaseCase import Test_BaseCase, res_to_dict


"""
This is a TestCase object to test the functions in questionsController.py
"""
class Test_questionsController(Test_BaseCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # test the GET request for QuestionAPI
    def test_QuestionAPI_GET(self):

        # request has invalid params input
        response = self.app.get('/questions?id=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record not found
        response = self.app.get('/questions?id=10')
       # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 404)
        
        # success case
        response = self.app.get('/questions?id=1')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['id'], 1)
        self.assertEqual(res['description'], 'description_1')

    # test the POST request for QuestionAPI
    def test_QuestionAPI_POST(self):

        # request has invalid params input
        response = self.app.post('/questions?topic_id=1&lesson_id=&description=description_6')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record not found
        response = self.app.post('/questions?topic_id=1&lesson_id=5&description=description_6')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 404)

        # success case
        response = self.app.post('/questions?topic_id=1&lesson_id=1&description=description_6')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['description'], 'description_6')

    # test the PUT request for QuestionAPI
    def test_QuestionAPI_PUT(self):

        # request has invalid params input
        response = self.app.put('/questions?id=1')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record not found
        response = self.app.put('/questions?id=6&description=description_new')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 404)

        # success case
        response = self.app.put('/questions?id=1&description=description_new')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['description'], 'description_new')

    # test the DELETE request for QuestionAPI
    def test_QuizAPI_DELETE(self):

        # request has invalid params input
        response = self.app.delete('/questions?id=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record not found
        response = self.app.delete('/questions?id=6')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 404)

        # success case
        response = self.app.delete('/questions?id=5')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['message'], 'Successfully deleted question')

    # test the GET request for QuestionGetAllAPI
    def test_QuestionGetAllAPI_GET(self):

        # success case
        response = self.app.get('/questions/all')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(len(res['questions']), 5)


if __name__ == '__main__':
    unittest.main(verbosity=2)
    