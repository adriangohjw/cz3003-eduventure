import sys
from os import path, getcwd
from flask import Flask
from flask import request
sys.path.append(getcwd())

import unittest

from services.core.contracts.lessons_contracts import *


class Test_lessons_contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def test_validate_topic_id(self):
        with self.assertRaises(TypeError):

            validate_topic_id(None)

        with self.assertRaises(ValueError):
            validate_topic_id("")

    def test_validate_lession_id(self):
        with self.assertRaises(TypeError):

            validate_lesson_id(None)

        with self.assertRaises(ValueError):
            validate_lesson_id("")

    def test_validate_name(self):
        with self.assertRaises(TypeError):

            validate_name(None)

        with self.assertRaises(ValueError):
            validate_name("")

    def test_validate_content(self):
        with self.assertRaises(TypeError):

            validate_content(None)

        with self.assertRaises(ValueError):
            validate_content("")

    def test_lessonReadContract(self):
        app = Flask(__name__)
        with app.test_request_context('/?topic_id=12&lesson_id=1', method='POST'):
            self.assertEqual(lessonReadContract(request), { 'topic_id':'12','lesson_id': '1' })

        with app.test_request_context('/?topic_id=12&lesson_id=', method='POST'):
            # now you can do something with the request until the
            # end of the with block, such as basic assertions:
            # assert request.path == '/hello'
            with self.assertRaises(ValueError):
                lessonReadContract(request)

    def test_lessonCreateContract(self):
        app = Flask(__name__)
        with app.test_request_context('/?topic_id=12&name=se&content=secontent', method='POST'):
            self.assertEqual(lessonCreateContract(request), { 'topic_id':'12','name': 'se','content':'secontent' })

        with app.test_request_context('/?topic_id=12&name=se&content=', method='POST'):
            # now you can do something with the request until the
            # end of the with block, such as basic assertions:
            # assert request.path == '/hello'
            with self.assertRaises(ValueError):
                lessonCreateContract(request)

    def test_lessonUpdateContract(self):
        app = Flask(__name__)
        with app.test_request_context('/?topic_id=12&lesson_id=1&col=name&value=3', method='POST'):
            self.assertEqual(lessonUpdateContract(request), { 'topic_id': '12',
        'lesson_id': '1',
        'col': 'name',
        'value': '3'       })

        with app.test_request_context('/?topic_id=12&lesson_id=1&col=name&value=', method='POST'):
            # now you can do something with the request until the
            # end of the with block, such as basic assertions:
            # assert request.path == '/hello'
            with self.assertRaises(ValueError):
                lessonUpdateContract(request)

    def test_lessonDeleteContract(self):
        app = Flask(__name__)
        with app.test_request_context('/?topic_id=12&lesson_id=1', method='POST'):
            self.assertEqual(lessonReadContract(request), { 'topic_id':'12','lesson_id': '1' })

        with app.test_request_context('/?topic_id=12&lesson_id=', method='POST'):
            # now you can do something with the request until the
            # end of the with block, such as basic assertions:
            # assert request.path == '/hello'
            with self.assertRaises(ValueError):
                lessonReadContract(request)

if __name__ == '__main__':
    unittest.main()
