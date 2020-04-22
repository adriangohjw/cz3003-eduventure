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

from services.core.contracts.lessons_contracts import (
    validate_topic_id, 
    validate_content, 
    validate_name, 
    validate_lesson_id,
    validate_url_link, 
    lessonCreateContract, 
    lessonDeleteContract, 
    lessonReadContract, 
    lessonUpdateContract
)
    

"""
This is a TestCase object to test the functions in lessons_contracts.py
"""
class Test_lessons_contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # test the function validate_lesson_id
    def test_validate_lesson_id(self):
        print('\r')

        # check if TypeError raised when arg is None type
        print('--- test if arg is None type')
        self.assertRaises(TypeError, validate_lesson_id, None)

        # check if TypeError raised when arg is string type
        print('--- test if arg is string type')
        self.assertRaises(TypeError, validate_lesson_id, 'testing')

        # check if TypeError raised when arg is float type
        print('--- test if arg is float type')
        self.assertRaises(TypeError, validate_lesson_id, 1.1)

        # check if TypeError raised when arg is boolean type
        print('--- test if arg is boolean type')
        self.assertRaises(TypeError, validate_lesson_id, True)

    # test the function validate_name
    def test_validate_name(self):
        print('\r')

        # check if TypeError raised when arg is None type
        print('--- test if arg is None type')
        self.assertRaises(TypeError, validate_name, None)

        # check if ValueError raised when arg is empty string
        print('--- test if arg is empty string')
        self.assertRaises(ValueError, validate_name, '')

    # test the function validate_content
    def test_validate_content(self):
        print('\r')

        # check if TypeError raised when arg is None type
        print('--- test if arg is None type')
        self.assertRaises(TypeError, validate_content, None)

        # check if ValueError raised when arg is empty string
        print('--- test if arg is empty string')
        self.assertRaises(ValueError, validate_content, '')

    # test the function validate_url_link
    def test_validate_url_link(self):
        print('\r')

        # check if ValueError raised when arg is empty string
        print('--- test if arg is empty string')
        self.assertRaises(ValueError, validate_url_link, '')

        # check if ValueError raised when arg is in the wrong format
        print('--- test if arg is in the wrong format (no https://)')
        self.assertRaises(ValueError, validate_url_link, 'www.google.com')

    # test the function lessonReadContract
    def test_lessonReadContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?topic_id=12&lesson_id=1', method='GET'):
            # check res returned by func is correct
            self.assertEqual(
                lessonReadContract(request), 
                {
                    'topic_id': 12,
                    'lesson_id': 1
                }
            )

        # passing request with unacceptable value in params (no value passed into 'lesson_id')
        print('--- test request with unacceptable params value (no value for \'lesson_id\')')
        with app.test_request_context('/?topic_id=12&lesson_id=', method='GET'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, lessonReadContract, request)

    # test the function lessonCreateContract
    def test_lessonCreateContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?topic_id=12&name=se&content=secontent&url_link=https%3A%2F%2Fwww.google.com', method='POST'):
            # check res returned by func is correct
            self.assertEqual(
                lessonCreateContract(request), 
                {
                    'topic_id': 12,
                    'name': 'se',
                    'content':'secontent',
                    'url_link': 'https://www.google.com'
                }
            )

        # passing request with missing params ('content' param missing)
        print('--- test request with missing params (\'content\')')
        with app.test_request_context('/?topic_id=12&name=se', method='POST'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, lessonCreateContract, request)

        # passing request with unacceptable value in params (empty string passed into 'content')
        print('--- test request with unacceptable params value (empty string for \'content\')')
        with app.test_request_context('/?topic_id=12&name=se&content=', method='POST'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, lessonCreateContract, request)

    # test the function lessonUpdateContract
    def test_lessonUpdateContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?topic_id=12&lesson_id=1&col=name&value=3', method='PUT'):
            # check res returned by func is correct
            self.assertEqual(
                lessonUpdateContract(request), 
                { 
                    'topic_id': 12,
                    'lesson_id': 1,
                    'col': 'name',
                    'value': '3'       
                }
            )
            
        # passing request with missing params ('value' param missing)
        print('--- test request with missing params (\'value\')')
        with app.test_request_context('/?topic_id=12&lesson_id=1&col=name', method='PUT'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, lessonUpdateContract, request)

        # passing request with unacceptable value in params (no value passed into 'value')
        print('--- test request with unacceptable params value (no value for \'value\')')
        with app.test_request_context('/?topic_id=12&lesson_id=1&col=name&value=', method='PUT'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, lessonUpdateContract, request)
        
        # passing request with unacceptable value in params (string type passed in)
        print('--- test request with unacceptable params value (string type for \'topic_id\')')
        with app.test_request_context('/?topic_id=hello&lesson_id=1&col=name&value=3', method='PUT'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, lessonUpdateContract, request)

    # test the function lessonDeleteContract
    def test_lessonDeleteContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?topic_id=12&lesson_id=1', method='DELETE'):
            # check res returned by func is correct
            self.assertEqual(
                lessonDeleteContract(request), 
                {
                    'topic_id': 12,
                    'lesson_id': 1 
                }
            )

        # passing request with missing params ('lesson_id' param missing)
        print('--- test request with missing params (\'lesson_id\')')
        with app.test_request_context('/?topic_id=12', method='DELETE'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, lessonDeleteContract, request)

        # passing request with unacceptable value in params (no value passed into 'lesson_id')
        print('--- test request with unacceptable params value (no value for \'lesson_id\')')
        with app.test_request_context('/?topic_id=12&lesson_id=', method='DELETE'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, lessonDeleteContract, request)


if __name__ == '__main__':
    unittest.main(verbosity=2)
