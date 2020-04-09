import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest 

from services.core.operations.tests.test_courses_operations import Test_courses_operations
from services.core.operations.tests.test_lessons_operations import Test_lessons_operations
from services.core.operations.tests.test_questionAttempts_operations import Test_questionAttempts_operations
from services.core.operations.tests.test_quizAttempts_operations import Test_quizAttempts_operations
from services.core.operations.tests.test_rs_lesson_quiz_contains_operations import Test_rs_lesson_quiz_contains_operations
from services.core.operations.tests.test_rs_staff_course_teaches_operations import Test_rs_staff_course_teaches_operations
from services.core.operations.tests.test_rs_student_course_enrols_operations import Test_rs_student_course_enrols_operations
from services.core.operations.tests.test_staffs_operations import Test_staffs_operations
from services.core.operations.tests.test_student_operations import Test_students_operations
from services.core.operations.tests.test_topics_operations import Test_topics_operations
from services.core.operations.tests.test_users_operations import Test_users_operations

if __name__ == '__main__':
    unittest.main()
