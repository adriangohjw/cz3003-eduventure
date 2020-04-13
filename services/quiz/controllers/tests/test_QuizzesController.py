import sys
from os import path, getcwd
sys.path.append(getcwd())

from flask import request
import unittest

from models import db
from run_test import create_app

from test_BaseCase import Test_BaseCase, res_to_dict


class Test_quizzesController(Test_BaseCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    
    def test_QuizAPI_GET(self):

        # invalid params input
        response = self.app.get('/quizzes?id=')
        self.assertEqual(response.status_code, 400)

        # record not found
        response = self.app.get('/quizzes?id=4')
        self.assertEqual(response.status_code, 404)
        
        # success case
        response = self.app.get('/quizzes?id=1')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['name'], 'quiz_1')


    def test_QuizAPI_POST(self):

        # invalid params input
        response = self.app.post('/quizzes?staff_id=3&name=quiz_4&is_fast=true&date_start=2020-01-01&date_end=')
        self.assertEqual(response.status_code, 400)

        # invalid params input (date_start > date_end)
        response = self.app.post('/quizzes?staff_id=3&name=quiz_4&is_fast=true&date_start=2020-01-31&date_end=2020-01-01')
        self.assertEqual(response.status_code, 412)

        # dependencies record not found
        response = self.app.post('/quizzes?staff_id=4&name=quiz_4&is_fast=true&date_start=2020-01-01&date_end=2020-01-31')
        self.assertEqual(response.status_code, 404)

        # success case
        response = self.app.post('/quizzes?staff_id=3&name=quiz_4&is_fast=true&date_start=2020-01-01&date_end=2020-01-31')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['name'], 'quiz_4')


    def test_QuizAPI_PUT(self):

        # invalid params input
        response = self.app.put('/quizzes?id=1')
        self.assertEqual(response.status_code, 400)

        # record not found
        response = self.app.put('/quizzes?id=4&name=quiz_new')
        self.assertEqual(response.status_code, 404)

        # success case
        import datetime
        from dateutil.parser import parse

        response = self.app.put('/quizzes?id=1&name=quiz_new&date_start=2020-01-01')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['name'], 'quiz_new')
        self.assertEqual(res['is_fast'], True)
        self.assertEqual(res['date_start'], 'Wed, 01 Jan 2020 00:00:00 GMT')
        self.assertEqual(res['date_end'], 'Tue, 31 Mar 2020 00:00:00 GMT')


    def test_QuizAPI_DELETE(self):

        # invalid params input
        response = self.app.delete('/quizzes?id=')
        self.assertEqual(response.status_code, 400)

        # record not found
        response = self.app.delete('/quizzes?id=4')
        self.assertEqual(response.status_code, 404)

        # success case
        response = self.app.delete('/quizzes?id=3')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['message'], 'Successfully deleted quiz')

        from models import Quiz
        quiz = Quiz.query.filter_by(id=3).first()
        self.assertIsNone(quiz)


    def test_QuizOverallAPI_GET(self):

        # invalid params input
        response = self.app.get('/quizzes/overall?id=')
        self.assertEqual(response.status_code, 400)

        # record not found
        response = self.app.get('/quizzes/overall?id=4')
        self.assertEqual(response.status_code, 404)
        
        # success case
        response = self.app.get('/quizzes/overall?id=1')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['name'], 'quiz_1')
        self.assertEqual(len(res['attempts']), 1)

        response = self.app.get('/quizzes/overall?id=2')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['name'], 'quiz_2')
        self.assertEqual(res['message'], 'No attempts recorded at the moment')


    def test_Quiz_CourseManagerAPI_GET(self):
        
        # invalid params input
        response = self.app.get('/quizzes/courses?quiz_id=')
        self.assertEqual(response.status_code, 400)

        # record not found
        response = self.app.get('/quizzes/courses?quiz_id=4')
        self.assertEqual(response.status_code, 404)
        
        # success case
        response = self.app.get('/quizzes/courses?quiz_id=1')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['count_attempts'], 1)

        response = self.app.get('/quizzes/courses?quiz_id=2')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['count_attempts'], 0)


    def test_Quiz_CourseManagerAPI_POST(self):

        # invalid params input
        response = self.app.post('/quizzes/courses?quiz_id=1&course_index=')
        self.assertEqual(response.status_code, 400)

        # dependencies record not found
        response = self.app.post('/quizzes/courses?quiz_id=4&course_index=cz1005')
        self.assertEqual(response.status_code, 404)

        # success case
        from models import Course 
        course = Course('cz1003')
        db.session.add(course)
        db.session.commit()

        response = self.app.post('/quizzes/courses?quiz_id=1&course_index=cz1003')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)


    def test_Quiz_QuestionManagerAPI_GET(self):

        # invalid params input
        response = self.app.get('/quizzes/questions?quiz_id=')
        self.assertEqual(response.status_code, 400)

        # record not found
        response = self.app.get('/quizzes/questions?quiz_id=4')
        self.assertEqual(response.status_code, 404)
        
        # success case
        response = self.app.get('/quizzes/questions?quiz_id=1')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res['questions']), 1)

        response = self.app.get('/quizzes/questions?quiz_id=2')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res['questions']), 0)


    def test_Quiz_QuestionManagerAPI_POST(self):

        # invalid params input
        response = self.app.post('/quizzes/questions?quiz_id=1&question_id=')
        self.assertEqual(response.status_code, 400)

        # dependencies record not found
        response = self.app.post('/quizzes/questions?quiz_id=4&question_id=1')
        self.assertEqual(response.status_code, 404)

        # success case
        from models import Quiz 
        quiz = Quiz.query.filter_by(id=2).first() 
        self.assertEqual(len(quiz.questions), 0)

        response = self.app.post('/quizzes/questions?quiz_id=2&question_id=1')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)


    def test_Quiz_QuestionManagerAPI_DELETE(self):

        # invalid params input
        response = self.app.delete('/quizzes/questions?quiz_id=1&question_id=')
        self.assertEqual(response.status_code, 400)

        # record not found
        response = self.app.delete('/quizzes/questions?quiz_id=4&question_id=1')
        self.assertEqual(response.status_code, 404)

        # success case
        from models import Quiz
        quiz = Quiz.query.filter_by(id=1).first()
        self.assertEqual(len(quiz.questions), 1)

        response = self.app.delete('/quizzes/questions?quiz_id=1&question_id=1')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['message'], 'Successfully deleted question from quiz')

        quiz = Quiz.query.filter_by(id=1).first()
        self.assertEqual(len(quiz.questions), 0)

        
if __name__ == '__main__':
    unittest.main()
    