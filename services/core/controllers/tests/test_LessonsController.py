
import sys
from os import path, getcwd
sys.path.append(getcwd())

from flask import request
import unittest

from models import db
from run_test import create_app

from test_BaseCase import Test_BaseCase, res_to_dict


class Test_lessonsController(Test_BaseCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def test_LessonAPI_GET(self):

        # invalid params input
        response = self.app.get('/lessons?topic_id=1&lesson_id=')
        self.assertEqual(response.status_code, 400)

        # record not found
        response = self.app.get('/lessons?topic_id=3&lesson_id=1')
        self.assertEqual(response.status_code, 404)
        
        # success case
        response = self.app.get('/lessons?topic_id=1&lesson_id=1')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['name'], 'lesson_1')


    def test_LessonAPI_POST(self):

        # invalid params input
        response = self.app.post('/lessons?topic_id=1&name=new_lesson')
        self.assertEqual(response.status_code, 400)

        # existing record
        response = self.app.post('/lessons?topic_id=1&name=lesson_1&content=content&url_link=https%3A%2F%2Fwww.google.com')
        self.assertEqual(response.status_code, 412)

         # success case
        response = self.app.post('/lessons?topic_id=2&name=lesson_5&content=content')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['name'], 'lesson_5')
        self.assertEqual(res['url_link'], None)

        response = self.app.post('/lessons?topic_id=2&name=lesson_6&content=content&url_link=https%3A%2F%2Fwww.google.com')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['name'], 'lesson_6')
        self.assertEqual(res['url_link'], 'https://www.google.com')


    def test_LessonListAPI_PUT(self):

        # invalid params input
        response = self.app.put('/lessons?topic_id=1&lesson_id=1&col=wrong_value&value=hello')
        self.assertEqual(response.status_code, 400)

        # record not found
        response = self.app.put('/lessons?topic_id=3&lesson_id=1&col=name&value=lesson_10')
        self.assertEqual(response.status_code, 404)

        # success case
        response = self.app.put('/lessons?topic_id=1&lesson_id=1&col=name&value=lesson_10')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['name'], 'lesson_10')

        response = self.app.put('/lessons?topic_id=1&lesson_id=1&col=content&value=content_new')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['content'], 'content_new')

        response = self.app.put('/lessons?topic_id=1&lesson_id=1&col=url_link&value=https%3A%2F%2Fwww.facebook.com')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['url_link'], 'https://www.facebook.com')

    
    def test_LessonListAPI_DELETE(self):
        
        # invalid params input
        response = self.app.delete('/lessons?topic_id=2&lesson_id=')
        self.assertEqual(response.status_code, 400)

        # record not found
        response = self.app.delete('/lessons?topic_id=2&lesson_id=2')
        self.assertEqual(response.status_code, 404)

        # success case
        response = self.app.delete('/lessons?topic_id=2&lesson_id=1')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['message'], 'Successfully deleted lesson')

        from models import Lesson
        lesson = Lesson.query.filter_by(topic_id=2).filter_by(id=1).first()
        self.assertIsNone(lesson)


    def test_LessonListAPI_GET(self):
        
        # success case
        response = self.app.get('/lessons/all')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res['lessons']), 4)
        self.assertEqual(res['lessons'][0]['name'], 'lesson_1')
        self.assertEqual(res['lessons'][1]['name'], 'lesson_2')


    def test_lesson_QuizManagerAPI_GET(self):

        # invalida params input
        response = self.app.get('/lessons/quizzes?topic_id=1')
        self.assertEqual(response.status_code, 400)

        # dependencies record not found
        response = self.app.get('/lessons/quizzes?topic_id=2&lesson_id=2')
        self.assertEqual(response.status_code, 404)

        # relationship record not found
        response = self.app.get('/lessons/quizzes?topic_id=1&lesson_id=2')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(res['error'], 'No rs found')
        
        # success case
        response = self.app.get('/lessons/quizzes?topic_id=1&lesson_id=1')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res['quiz']), 2)


    def test_lesson_QuizManagerAPI_POST(self):

        # invalid params input
        response = self.app.post('/lessons/quizzes?topic_id=1')
        self.assertEqual(response.status_code, 400)

        # dependencies record not found
        response = self.app.post('/lessons/quizzes?topic_id=2&lesson_id=2&quiz_id=1')
        self.assertEqual(response.status_code, 400)

        # existing record found
        response = self.app.post('/lessons/quizzes?topic_id=1&lesson_id=1&quiz_id=1')
        self.assertEqual(response.status_code, 400)
        db.session.rollback()

        # success case 
        response = self.app.post('/lessons/quizzes?topic_id=2&lesson_id=1&quiz_id=1')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['topic_id'], 2)
        self.assertEqual(res['lesson_id'], 1)
        self.assertEqual(res['quiz_id'], 1)

        from models import Rs_lesson_quiz_contain
        rs = Rs_lesson_quiz_contain.query.filter_by(topic_id=2).filter_by(lesson_id=1).filter_by(quiz_id=1).all()
        self.assertEqual(len(rs), 1)


    def test_lesson_QuizManagerAPI_DELETE(self):

        # invalid params input
        response = self.app.delete('/lessons/quizzes?id=')
        self.assertEqual(response.status_code, 400)

        # record not found
        response = self.app.delete('/lessons/quizzes?id=4')
        self.assertEqual(response.status_code, 404)

        # success case
        response = self.app.delete('/lessons/quizzes?id=1')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['message'], 'Successfully deleted rs')

        from models import Rs_lesson_quiz_contain
        rs = Rs_lesson_quiz_contain.query.filter_by(id=1).first()
        self.assertIsNone(rs)


if __name__ == '__main__':
    unittest.main()
    