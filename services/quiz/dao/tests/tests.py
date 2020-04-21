import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest 

from services.quiz.dao.tests.test_QuizzesDao import Test_quizzes_dao
from services.quiz.dao.tests.test_QuestionsDAO import Test_QuestionsDAO
from services.quiz.dao.tests.test_QuestionChoicesDAO import Test_QuestionChoicesDAO
from services.quiz.dao.tests.test_RsQuizCourseAssignDAO import Test_RsQuizCourseAssignDAO
from services.quiz.dao.tests.test_RsQuizQuestionContainDAO import Test_RsQuizQuestionContainDAO

if __name__ == '__main__':
    unittest.main(verbosity=2)
