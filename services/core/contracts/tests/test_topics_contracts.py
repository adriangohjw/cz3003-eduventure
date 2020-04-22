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

from services.core.contracts.topics_contracts import (
    validate_name, 
    validate_id, 
    topicReadContract,
    topicCreateContract, 
    topicUpdateContract, 
    topicDeleteContract
)    


"""
This is a TestCase object to test the functions in topic_contracts.py
"""
class Test_topics_contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # test the function validate_id
    def test_validate_id(self):
        print('\r')

        # check if TypeError raised when arg is None type
        print('--- test if arg is None type')
        self.assertRaises(TypeError, validate_id, None)

        # check if TypeError raised when arg is string type
        print('--- test if arg is string type')
        self.assertRaises(TypeError, validate_id, 'testing')

        # check if TypeError raised when arg is float type
        print('--- test if arg is float type')
        self.assertRaises(TypeError, validate_id, 1.1)

        # check if TypeError raised when arg is boolean type
        print('--- test if arg is boolean type')
        self.assertRaises(TypeError, validate_id, True)

    # test the function validate_name
    def test_validate_name(self):
        print('\r')

        # check if TypeError raised when arg is None type
        print('--- test if arg is None type')
        self.assertRaises(TypeError, validate_name, None)

        # check if ValueError raised when arg is empty string
        print('--- test if arg is empty string')
        self.assertRaises(ValueError, validate_name, '')

    # test the function topicReadContract
    def test_topicReadContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?id=2', method='GET'):
            # check res returned by func is correct
            self.assertEqual(
                topicReadContract(request), 
                {
                    'id': 2
                }
            )

        # passing request with unacceptable value in params (no value passed into 'id')
        print('--- test request with unacceptable params value (no value for \'id\')')
        with app.test_request_context('/?id=', method='GET'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, topicReadContract, request)

        # passing request with unacceptable value in params (string type passed in)
        print('--- test request with unacceptable params value (string type for \'id\')')
        with app.test_request_context('/?id=hello', method='GET'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, topicReadContract, request)

    # test the function topiCreateContract
    def test_topicCreateContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?name=joe', method='POST'):
            # check res returned by func is correct
            self.assertEqual(
                topicCreateContract(request), 
                {
                    'name':'joe'
                }
            )

        # passing request with unacceptable value in params (empty string passed into 'name')
        print('--- test request with unacceptable params value (empty string for \'name\')')
        with app.test_request_context('/?name=', method='POST'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, topicCreateContract, request)
    
    # test the function topicUpdateContract
    def test_topicUpdateContract(self):
        print('\r')
        
        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?id=1&name=topic_1', method='PUT'):
            # check res returned by func is correct
            self.assertEqual(
                topicUpdateContract(request), 
                {
                    'id': 1,
                    'name':'topic_1'
                }
            )

        # passing request with unacceptable value in params (empty string passed into 'name')
        print('--- test request with unacceptable params value (empty string for \'name\')')
        with app.test_request_context('/?id=1&name=', method='PUT'):
            # check if ValueError is being raise
            self.assertRaises(ValueError, topicUpdateContract, request)

        # passing request with unacceptable value in params (no value passed into 'id')
        print('--- test request with unacceptable params value (no value for \'id\')')
        with app.test_request_context('/?id=&name=topic_1', method='PUT'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, topicUpdateContract, request)

    # test the function topicDeleteContract
    def test_topicDeleteContract(self):
        print('\r')

        # passing request with acceptable value
        print('--- test acceptable request')
        with app.test_request_context('/?id=1', method='DELETE'):
            # check res returned by func is correct
            self.assertEqual(
                topicDeleteContract(request), 
                {
                    'id': 1                
                }
            )

        # passing request with unacceptable value in params (no value passed into 'id')
        print('--- test request with unacceptable params value (no value for \'id\')')
        with app.test_request_context('/?id=', method='DELETE'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, topicDeleteContract, request)

        # passing request with unacceptable value in params (string type passed in)
        print('--- test request with unacceptable params value (string type for \'id\')')
        with app.test_request_context('/?id=hello', method='DELETE'):
            # check if TypeError is being raise
            self.assertRaises(TypeError, topicDeleteContract, request)


if __name__ == '__main__':
    unittest.main(verbosity=2)
