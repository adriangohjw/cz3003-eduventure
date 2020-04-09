import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest 

from services.core.contracts.tests.test_courses_contracts import Test_courses_contracts
from services.core.contracts.tests.test_courses_contracts import Test_courses_contracts
from services.core.contracts.tests.test_lessons_contracts import Test_lessons_contracts
from services.core.contracts.tests.test_questionAttempts_contracts import Test_questionAttempts_contracts
from services.core.contracts.tests.test_quizAttempts_contracts import Test_quizAttempts_contracts
from services.core.contracts.tests.test_rs_lesson_quiz_contains_contracts import Test_rs_lesson_quiz_contains_contracts
from services.core.contracts.tests.test_rs_staff_course_teaches_contracts import Test_rs_staff_course_teaches_contracts
from services.core.contracts.tests.test_rs_student_course_enrols_contracts import Test_rs_student_course_enrols_contracts
from services.core.contracts.tests.test_staffs_contracts import Test_staffs_contracts
from services.core.contracts.tests.test_students_contracts import Test_students_contracts
from services.core.contracts.tests.test_topics_contracts import Test_topics_contracts
from services.core.contracts.tests.test_users_contracts import Test_user_contracts

if __name__ == '__main__':
    unittest.main()
