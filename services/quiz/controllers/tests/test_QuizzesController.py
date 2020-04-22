import sys
from os import path, getcwd
sys.path.append(getcwd())

from flask import request
import unittest

from models import db, Course
from run_test import create_app

from test_BaseCase import Test_BaseCase, res_to_dict

import datetime
from dateutil.parser import parse


"""
This is a TestCase object to test the functions in quizzesController.py
"""
class Test_quizzesController(Test_BaseCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # test the GET request for QuizAPI
    def test_QuizAPI_GET(self):

        # request has invalid params input
        response = self.app.get('/quizzes?id=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record not found
        response = self.app.get('/quizzes?id=4')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 404)
        
        # success case
        response = self.app.get('/quizzes?id=1')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['name'], 'quiz_1')

    # test the POST request for QuizAPI
    def test_QuizAPI_POST(self):

        # request has invalid params input
        response = self.app.post('/quizzes?staff_id=3&name=quiz_4&is_fast=true&date_start=2020-01-01&date_end=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request has invalid params input (date_start > date_end)
        response = self.app.post('/quizzes?staff_id=3&name=quiz_4&is_fast=true&date_start=2020-01-31&date_end=2020-01-01')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input - date_start after date_end)')
        self.assertEqual(response.status_code, 412)

        # request error as dependency record not found
        response = self.app.post('/quizzes?staff_id=4&name=quiz_4&is_fast=true&date_start=2020-01-01&date_end=2020-01-31')
        # check if status code is correct
        print('--- check if status code is correct (dependency record not found)')
        self.assertEqual(response.status_code, 404)

        # success case
        response = self.app.post('/quizzes?staff_id=3&name=quiz_4&is_fast=true&date_start=2020-01-01&date_end=2020-01-31')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['name'], 'quiz_4')

    # test the PUT request for QuizAPI
    def test_QuizAPI_PUT(self):

        # request has invalid params input
        response = self.app.put('/quizzes?id=1')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record not found
        response = self.app.put('/quizzes?id=4&name=quiz_new')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 404)

        # success case
        response = self.app.put('/quizzes?id=1&name=quiz_new&date_start=2020-01-01')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['name'], 'quiz_new')
        self.assertEqual(res['is_fast'], True)
        self.assertEqual(res['date_start'], 'Wed, 01 Jan 2020 00:00:00 GMT')
        self.assertEqual(res['date_end'], 'Tue, 31 Mar 2020 00:00:00 GMT')

    # test the DELETE request for QuizAPI
    def test_QuizAPI_DELETE(self):

        # request has invalid params input
        response = self.app.delete('/quizzes?id=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record not found
        response = self.app.delete('/quizzes?id=4')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 404)

        # success case
        response = self.app.delete('/quizzes?id=3')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')
        self.assertEqual(res['message'], 'Successfully deleted quiz')

    # test the GET request for QuizOverallAPI
    def test_QuizOverallAPI_GET(self):

        # request has invalid params input
        response = self.app.get('/quizzes/overall?id=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record not found
        response = self.app.get('/quizzes/overall?id=4')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 404)
        
        # success case (1)
        response = self.app.get('/quizzes/overall?id=1')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (2), check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful (1), check if JSON returned is correct')
        self.assertEqual(res['name'], 'quiz_1')
        self.assertEqual(len(res['attempts']), 1)

        # success case (2)
        response = self.app.get('/quizzes/overall?id=2')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (2), check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful (2), check if JSON returned is correct')
        self.assertEqual(res['name'], 'quiz_2')
        self.assertEqual(res['message'], 'No attempts recorded at the moment')

    # test the GET request for CourseManagerAPI
    def test_Quiz_CourseManagerAPI_GET(self):
        
        # request has invalid params input
        response = self.app.get('/quizzes/courses?quiz_id=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record not found
        response = self.app.get('/quizzes/courses?quiz_id=4')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 404)
        
        # success case (1)
        response = self.app.get('/quizzes/courses?quiz_id=1')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (1), check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful (1), check if JSON returned is correct')
        self.assertEqual(res['count_attempts'], 1)

        # success case (2)
        response = self.app.get('/quizzes/courses?quiz_id=2')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (2), check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful (2), check if JSON returned is correct')
        self.assertEqual(res['count_attempts'], 0)

    # test the POST request for CourseManagerAPI
    def test_Quiz_CourseManagerAPI_POST(self):

        # request has invalid params input
        response = self.app.post('/quizzes/courses?quiz_id=1&course_index=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as dependency record not found
        response = self.app.post('/quizzes/courses?quiz_id=4&course_index=cz1005')
        # check if status code is correct
        print('--- check if status code is correct (dependency record not found)')
        self.assertEqual(response.status_code, 404)

        # adding courses
        course = Course('cz1003')
        db.session.add(course)
        db.session.commit()

        # success case
        response = self.app.post('/quizzes/courses?quiz_id=1&course_index=cz1003')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (2), check if status code is correct')
        self.assertEqual(response.status_code, 200)

    # test the GET request for QuestionManagerAPI
    def test_Quiz_QuestionManagerAPI_GET(self):

        # request has invalid params input
        response = self.app.get('/quizzes/questions?quiz_id=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record not found
        response = self.app.get('/quizzes/questions?quiz_id=4')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 404)
        
        # success case (1)
        response = self.app.get('/quizzes/questions?quiz_id=1')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (1), check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful (1), check if JSON returned is correct')
        self.assertEqual(len(res['questions']), 1)

        # success case (2)
        response = self.app.get('/quizzes/questions?quiz_id=2')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful (2), check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful (2), check if JSON returned is correct')
        self.assertEqual(len(res['questions']), 0)

    # test the POST request for QuestionManagerAPI
    def test_Quiz_QuestionManagerAPI_POST(self):

        # request has invalid params input
        response = self.app.post('/quizzes/questions?quiz_id=1&question_id=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as dependency record not found
        response = self.app.post('/quizzes/questions?quiz_id=4&question_id=1')
        # check if status code is correct
        print('--- check if status code is correct (dependency record not found)')
        self.assertEqual(response.status_code, 404)

        # success case
        response = self.app.post('/quizzes/questions?quiz_id=2&question_id=1')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        print('--- successful, check if JSON returned is correct')

    # test the DELETE request for QuestionManagerAPI
    def test_Quiz_QuestionManagerAPI_DELETE(self):

        # request has invalid params input
        response = self.app.delete('/quizzes/questions?quiz_id=1&question_id=')
        # check if status code is correct
        print('--- check if status code is correct (invalid params input)')
        self.assertEqual(response.status_code, 400)

        # request error as record not found
        response = self.app.delete('/quizzes/questions?quiz_id=4&question_id=1')
        # check if status code is correct
        print('--- check if status code is correct (record not found)')
        self.assertEqual(response.status_code, 404)

        # success case
        response = self.app.delete('/quizzes/questions?quiz_id=1&question_id=1')
        res = res_to_dict(response) # convert response to dictionary
        # check if status code is correct
        print('--- successful, check if status code is correct')
        self.assertEqual(response.status_code, 200)
        # check if JSON returned is correct
        self.assertEqual(res['message'], 'Successfully deleted question from quiz')
        
        
if __name__ == '__main__':
    unittest.main(verbosity=2)
    