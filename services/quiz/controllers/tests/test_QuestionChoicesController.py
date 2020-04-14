import sys
from os import path, getcwd
sys.path.append(getcwd())

from flask import request
import unittest

from models import db
from run_test import create_app

from test_BaseCase import Test_BaseCase, res_to_dict


class Test_questionChoicesController(Test_BaseCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def test_QuestionChoiceAPI_GET(self):
        
        # invalid params input
        response = self.app.get('/question_choices?question_id=1&questionChoice_id=')
        self.assertEqual(response.status_code, 400)

        # record not found
        response = self.app.get('/question_choices?question_id=1&questionChoice_id=10')
        self.assertEqual(response.status_code, 404)
        
        # success case
        response = self.app.get('/question_choices?question_id=1&questionChoice_id=1')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['description'], 'choice_1')


    def test_QuestionChoiceAPI_POST(self):

        # invalid params input
        response = self.app.post('/question_choices?question_id=&description=choice_4&is_correct=true')
        self.assertEqual(response.status_code, 400)

        # dependencies record not found
        response = self.app.post('/question_choices?question_id=6&description=choice_4&is_correct=true')
        self.assertEqual(response.status_code, 404)

        # success case
        response = self.app.post('/question_choices?question_id=2&description=choice_4&is_correct=true')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['description'], 'choice_4')


    def test_QuestionChoiceAPI_PUT(self):

        # invalid params input
        response = self.app.put('/question_choices?question_id=1&questionChoice_id=&description=description_new&is_correct=true')
        self.assertEqual(response.status_code, 400)

        # record not found
        response = self.app.put('//question_choices?question_id=1&questionChoice_id=19&description=description_new&is_correct=true')
        self.assertEqual(response.status_code, 404)

        # success case
        response = self.app.put('/question_choices?question_id=1&questionChoice_id=1&description=description_new')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['description'], 'description_new')


    def test_QuestionChoiceAPI_DELETE(self):

        # invalid params input
        response = self.app.delete('/question_choices?question_id=1&questionChoice_id=')
        self.assertEqual(response.status_code, 400)

        # record not found
        response = self.app.delete('/question_choices?question_id=1&questionChoice_id=4')
        self.assertEqual(response.status_code, 404)

        # success case
        response = self.app.delete('/question_choices?question_id=1&questionChoice_id=3')
        res = res_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['message'], 'Successfully deleted question choice')

        from models import QuestionChoice
        questionChoice = QuestionChoice.query.filter_by(question_id=1).filter_by(id=3).first()
        self.assertIsNone(questionChoice)


if __name__ == '__main__':
    unittest.main()
    