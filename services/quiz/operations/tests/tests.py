import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest 

from services.quiz.operations.tests.test_questionChoices_operations import Test_questionChoices_operations
from services.quiz.operations.tests.test_questions_operations import Test_questions_operations
from services.quiz.operations.tests.test_quizzes_operations import Test_quizzes_operations
from services.quiz.operations.tests.test_rs_quiz_course_assigns_operations import Test_rs_quiz_course_assigns_operations
from services.quiz.operations.tests.test_rs_quiz_question_contains_operations import Test_rs_quiz_question_contains_operations

if __name__ == '__main__':
    unittest.main(verbosity=2)
