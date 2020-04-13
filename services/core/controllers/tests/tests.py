import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest

from services.core.controllers.tests.test_ChallengesController import Test_challengesController
from services.core.controllers.tests.test_CoursesController import Test_coursesController
from services.core.controllers.tests.test_LessonsController import Test_lessonsController
from services.core.controllers.tests.test_ProgressesController import Test_progressesController
from services.core.controllers.tests.test_QuestionAttemptsController import Test_questionAttemptsController
from services.core.controllers.tests.test_QuizAttemptsController import Test_quizAttemptsController
from services.core.controllers.tests.test_StudentsController import Test_studentsController
from services.core.controllers.tests.test_StudentsController import Test_studentsController
from services.core.controllers.tests.test_TopicsController import Test_topicsController
from services.core.controllers.tests.test_UsersController import Test_usersController

if __name__ == '__main__':
    unittest.main()
