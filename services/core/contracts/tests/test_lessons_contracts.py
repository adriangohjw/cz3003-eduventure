import sys
from os import path, getcwd
sys.path.append(getcwd())

from flask import request
import unittest

from models import db
from run_test import create_app
app = create_app()
app.app_context().push()
db.init_app(app)

from services.core.contracts.lessons_contracts import \
    validate_topic_id, validate_content, validate_name, validate_lesson_id, validate_url_link, \
    lessonCreateContract, lessonDeleteContract, lessonReadContract, lessonUpdateContract


class Test_lessons_contracts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def test_validate_lesson_id(self):

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


    def test_validate_url_link(self):

        with self.assertRaises(ValueError):
            validate_url_link("")
            validate_url_link("www.google.com")


    def test_lessonReadContract(self):

        with app.test_request_context('/?topic_id=12&lesson_id=1', method='GET'):
            self.assertEqual(
                lessonReadContract(request), 
                {
                    'topic_id': 12,
                    'lesson_id': 1
                }
            )

        with app.test_request_context('/?topic_id=12&lesson_id=', method='GET'):
            self.assertRaises(TypeError, lessonReadContract, request)


    def test_lessonCreateContract(self):

        with app.test_request_context('/?topic_id=12&name=se&content=secontent&url_link=https%3A%2F%2Fwww.google.com', method='POST'):
            self.assertEqual(
                lessonCreateContract(request), 
                {
                    'topic_id': 12,
                    'name': 'se',
                    'content':'secontent',
                    'url_link': 'https://www.google.com'
                }
            )

        with app.test_request_context('/?topic_id=12&name=se', method='POST'):
            self.assertRaises(TypeError, lessonCreateContract, request)

        with app.test_request_context('/?topic_id=12&name=se&content=', method='POST'):
            self.assertRaises(ValueError, lessonCreateContract, request)


    def test_lessonUpdateContract(self):
        with app.test_request_context('/?topic_id=12&lesson_id=1&col=name&value=3', method='PUT'):
            self.assertEqual(
                lessonUpdateContract(request), 
                { 
                    'topic_id': 12,
                    'lesson_id': 1,
                    'col': 'name',
                    'value': '3'       
                }
            )
            
        with app.test_request_context('/?topic_id=12&lesson_id=1&col=name', method='PUT'):
            self.assertRaises(TypeError, lessonUpdateContract, request)

        with app.test_request_context('/?topic_id=12&lesson_id=1&col=name&value=', method='PUT'):
            self.assertRaises(ValueError, lessonUpdateContract, request)
        
        with app.test_request_context('/?topic_id=hello&lesson_id=1&col=name&value=3', method='PUT'):
            self.assertRaises(TypeError, lessonUpdateContract, request)


    def test_lessonDeleteContract(self):
        with app.test_request_context('/?topic_id=12&lesson_id=1', method='DELETE'):
            self.assertEqual(
                lessonDeleteContract(request), 
                {
                    'topic_id': 12,
                    'lesson_id': 1 
                }
            )

        with app.test_request_context('/?topic_id=12', method='DELETE'):
            self.assertRaises(TypeError, lessonDeleteContract, request)

        with app.test_request_context('/?topic_id=12&lesson_id=', method='DELETE'):
            self.assertRaises(TypeError, lessonDeleteContract, request)


if __name__ == '__main__':
    unittest.main()
