import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest 

from services.quiz.contracts.tests.test_questionChoices_contracts import Test_questionChoices_contracts
from services.quiz.contracts.tests.test_questions_contracts import Test_questions_contracts
from services.quiz.contracts.tests.test_quizzes_contracts import Test_quizzes_contracts
from services.quiz.contracts.tests.test_rs_quiz_course_assigns_contracts import Test_rs_quiz_course_assigns_contracts
from services.quiz.contracts.tests.test_rs_quiz_question_contains_contracts import Test_rs_quiz_question_contains_contracts

if __name__ == '__main__':
    unittest.main(verbosity=2)
