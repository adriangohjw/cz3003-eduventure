import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest

from services.quiz.controllers.tests.test_QuestionsController import Test_questionsController
from services.quiz.controllers.tests.test_QuizzesController import Test_quizzesController

if __name__ == '__main__':
    unittest.main()
