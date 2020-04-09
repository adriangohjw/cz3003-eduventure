import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest 

from services.core.dao.tests.test_UsersDao import Test_users_dao
from services.core.dao.tests.test_CoursesDAO import Test_CoursesDAO
from services.core.dao.tests.test_LessonsDAO import Test_LessonsDAO
from services.core.dao.tests.test_QuestionAttemptsDAO import Test_QuestionAttemptsDAO
from services.core.dao.tests.test_QuizAttemptsDAO import Test_QuizAttemptsDAO
from services.core.dao.tests.test_RsStaffCourseTeachDAO import Test_RsStaffCourseTeachDAO
from services.core.dao.tests.test_RsStudentCourseEnrolDAO import Test_RsStudentCourseEnrolDAO
from services.core.dao.tests.test_StaffsDAO import Test_StaffsDAO
from services.core.dao.tests.test_StudentsDAO import Test_StudentsDAO
from services.core.dao.tests.test_TopicsDAO import Test_TopicsDAO

if __name__ == '__main__':
    unittest.main()
