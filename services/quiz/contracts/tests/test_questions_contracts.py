import sys
from os import path, getcwd
from flask import request
from flask import Flask

sys.path.append(getcwd())

import unittest

from services.quiz.contracts.questions_contracts import validate_description,validate_id,validate_lesson_id,validate_topic_id,questionCreateContract,questionDeleteContract,questionReadContract,questionUpdateContract
from models import db
from run_test import create_app

app = create_app()
app.app_context().push()
db.init_app(app)

class Test_questions_contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def test_validate_id(self):
        with self.assertRaises(Exception):
            validate_id(None)
            validate_id("")

    def test_validate_topic_id(self):
        with self.assertRaises(Exception):
            validate_topic_id(None)
            validate_topic_id("")

    def test_validate_lesson_id(self):
        with self.assertRaises(Exception):
            validate_lesson_id(None)
            validate_lesson_id("")

    def test_validate_description(self):
        with self.assertRaises(Exception):
            validate_description(None)
            validate_description("")

    def test_questionReadContract(self):
        with app.test_request_context('/?id=2', method='POST'):
            self.assertEqual(questionReadContract(request), { 'id': '2' })

        with app.test_request_context('/?id=', method='POST'):
            with self.assertRaises(Exception):
                questionReadContract(request)

    def test_questionCreateContract(self):
        with app.test_request_context('/?topic_id=1&lesson_id=2&description=hard', method='POST'):
            self.assertEqual(questionCreateContract(request), {'topic_id': '1',
        'lesson_id': '2',
        'description': 'hard' })

        with app.test_request_context('/?topic_id=1&lesson_id=2&description=', method='POST'):
            with self.assertRaises(Exception):
                questionCreateContract(request)

    def test_questionUpdateContract(self):
        with app.test_request_context('/?id=1&description=hard', method='POST'):
            self.assertEqual(questionUpdateContract(request), {'id': '1', 'description': 'hard' })

        with app.test_request_context('/?id=1&description=', method='POST'):
            with self.assertRaises(Exception):
                questionUpdateContract(request)

    def test_questionDeleteContract(self):
        with app.test_request_context('/?id=2', method='POST'):
            self.assertEqual(questionDeleteContract(request), { 'id': '2' })

        with app.test_request_context('/?id=', method='POST'):
            with self.assertRaises(Exception):
                questionDeleteContract(request)


if __name__ == '__main__':
    unittest.main()