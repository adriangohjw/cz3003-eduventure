import sys
from os import path, getcwd
sys.path.append(getcwd())

from flask import request
import unittest

from models import db
from run_test import create_app

from test_BaseCase import Test_BaseCase, res_to_dict


"""
This is a TestCase object to test the functions in questionChoicesController.py
"""
class Test_questionChoicesController(Test_BaseCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # test the GET request for QuestionChoiceAPI
    def test_QuestionChoiceAPI_GET(self):
        
        # request has invalid params input
        response = self.app.get('/question_choices?question_id=1&questionChoice_id=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record not found
        response = self.app.get('/question_choices?question_id=1&questionChoice_id=10')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 404)
        
        # success case
        response = self.app.get('/question_choices?question_id=1&questionChoice_id=1')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['description'], 'choice_1')

    # test the POST request for QuestionChoiceAPI
    def test_QuestionChoiceAPI_POST(self):

        # request has invalid params input
        response = self.app.post('/question_choices?question_id=&description=choice_4&is_correct=true')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # dependencies record not found
        response = self.app.post('/question_choices?question_id=6&description=choice_4&is_correct=true')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 404)

        # success case
        response = self.app.post('/question_choices?question_id=2&description=choice_4&is_correct=true')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['description'], 'choice_4')

    # test the PUT request for QuestionChoiceAPI
    def test_QuestionChoiceAPI_PUT(self):

        # request has invalid params input
        response = self.app.put('/question_choices?question_id=1&questionChoice_id=&description=description_new&is_correct=true')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record not found
        response = self.app.put('//question_choices?question_id=1&questionChoice_id=19&description=description_new&is_correct=true')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 404)

        # success case
        response = self.app.put('/question_choices?question_id=1&questionChoice_id=1&description=description_new')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['description'], 'description_new')

    # test the DELETE request for QuestionChoiceAPI
    def test_QuestionChoiceAPI_DELETE(self):

        # request has invalid params input
        response = self.app.delete('/question_choices?question_id=1&questionChoice_id=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record not found
        response = self.app.delete('/question_choices?question_id=1&questionChoice_id=4')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 404)

        # success case
        response = self.app.delete('/question_choices?question_id=1&questionChoice_id=3')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['message'], 'Successfully deleted question choice')


if __name__ == '__main__':
    unittest.main(verbosity=2)
    