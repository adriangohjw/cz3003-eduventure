import sys
from os import path, getcwd

sys.path.append(getcwd())
from flask import Flask
from flask import request
import unittest

from services.core.contracts.topics_contracts import validate_name,validate_id,topicCreateContract,topicReadContract


class Test_topics_contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def test_validate_id(self):
        with self.assertRaises(TypeError):
            validate_id(None)
            validate_id("testStr")
            validate_id(33.33)
            validate_id(True)

        with self.assertRaises(ValueError):
            validate_id("")

    def test_validate_name(self):
        with self.assertRaises(TypeError):
            validate_name(None)

        with self.assertRaises(ValueError):
            validate_name("")

    def test_topicReadContract(self):
        app = Flask(__name__)
        with app.test_request_context('/?id=2', method='POST'):
            self.assertEqual(topicReadContract(request), {'id':'2'})
        #test not passed as it throws a TypeError since id is not integer in validate_id()
        with app.test_request_context('/?id=', method='POST'):
            with self.assertRaises(ValueError):
                topicReadContract(request)

    def test_topicCreateContract(self):
        app = Flask(__name__)
        with app.test_request_context('/?name=joe', method='POST'):
            self.assertEqual(topicCreateContract(request), {'name':'joe'})

        with app.test_request_context('/?name=', method='POST'):
            with self.assertRaises(ValueError):
                topicCreateContract(request)

if __name__ == '__main__':
    unittest.main()
