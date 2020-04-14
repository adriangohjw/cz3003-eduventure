import sys
from os import path, getcwd
sys.path.append(getcwd())

from flask import request
import unittest

from models import db
from run_test import create_app

from test_BaseCase import Test_BaseCase, res_to_dict


class Test_questionsController(Test_BaseCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def test_QuestionAPI_GET(self):

        # invalid params input
        response = self.app.get('/questions?id=')
        self.assertEqual(response.status_code, 400)

        # record not found
        response = self.app.get('/questions?id=10')
        self.assertEqual(response.status_code, 404)
        
        # success case
        response = self.app.get('/questions?id=1')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['id'], 1)
        self.assertEqual(res['description'], 'description_1')


    def test_QuestionAPI_POST(self):

        # invalid params input
        response = self.app.post('/questions?topic_id=1&lesson_id=&description=description_6')
        self.assertEqual(response.status_code, 400)

        # dependencies record not found
        response = self.app.post('/questions?topic_id=1&lesson_id=5&description=description_6')
        self.assertEqual(response.status_code, 404)

        # success case
        response = self.app.post('/questions?topic_id=1&lesson_id=1&description=description_6')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['description'], 'description_6')

    
    def test_QuestionAPI_PUT(self):

        # invalid params input
        response = self.app.put('/questions?id=1')
        self.assertEqual(response.status_code, 400)

        # record not found
        response = self.app.put('/questions?id=6&description=description_new')
        self.assertEqual(response.status_code, 404)

        # success case
        response = self.app.put('/questions?id=1&description=description_new')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['description'], 'description_new')


    def test_QuizAPI_DELETE(self):

        # invalid params input
        response = self.app.delete('/questions?id=')
        self.assertEqual(response.status_code, 400)

        # record not found
        response = self.app.delete('/questions?id=6')
        self.assertEqual(response.status_code, 404)

        # success case
        response = self.app.delete('/questions?id=5')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['message'], 'Successfully deleted question')

        from models import Question
        question = Question.query.filter_by(id=5).first()
        self.assertIsNone(question)


    def test_QuestionGetAllAPI_GET(self):

        # success case
        response = self.app.get('/questions/all')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res['questions']), 5)


if __name__ == '__main__':
    unittest.main()
    