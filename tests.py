import unittest 
from flask import Flask
from config import Config

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

from services.core.contracts.tests.test_users_contracts import Test_user_contracts
from services.core.contracts.tests.test_courses_contracts import Test_courses_contracts
from services.core.contracts.tests.test_lessons_contracts import Test_lessons_contracts
from services.core.contracts.tests.test_questionAttempts_contracts import Test_questionAttempts_contracts
from services.core.contracts.tests.test_quizAttempts_contracts import Test_quizAttempts_contracts
from services.core.contracts.tests.test_students_contracts import Test_students_contracts
from services.core.contracts.tests.test_topics_contracts import Test_topics_contracts

from services.core.operations.tests.test_users_operations import Test_users_operations
from services.core.operations.tests.test_courses_operations import Test_courses_operations
from services.core.operations.tests.test_lessons_operations import Test_lessons_operations
from services.core.operations.tests.test_questionAttempts_operations import Test_questionAttempts_operations
from services.core.operations.tests.test_quizAttempts_operations import Test_quizAttempts_operations
from services.core.operations.tests.test_staffs_operations import Test_staffs_operations
from services.core.operations.tests.test_student_operations import Test_students_operations
from services.core.operations.tests.test_topics_operations import Test_topics_operations
from services.core.operations.tests.test_rs_student_course_enrols_operations import Test_rs_student_course_enrols_operations
from services.core.operations.tests.test_rs_staff_course_teaches_operations import Test_rs_staff_course_teaches_operations
from services.quiz.dao.tests.test_QuizzesDao import Test_quizzes_dao
from services.quiz.dao.tests.test_QuestionsDAO import Test_QuestionsDAO
from services.quiz.dao.tests.test_QuestionChoicesDAO import Test_QuestionChoicesDAO
from services.quiz.dao.tests.test_RsQuizCourseAssignDAO import Test_RsQuizCourseAssignDAO
from services.quiz.dao.tests.test_RsQuizQuestionContainDAO import Test_RsQuizQuestionContainDAO

from services.quiz.contracts.tests.test_questionChoices_contracts import Test_questionChoices_contracts
from services.quiz.contracts.tests.test_questions_contracts import Test_questions_contracts
from services.quiz.contracts.tests.test_quizzes_contracts import Test_quizzes_contracts
from services.quiz.contracts.tests.test_rs_quiz_course_assigns_contracts import Test_rs_quiz_course_assigns_contracts
from services.quiz.contracts.tests.test_rs_quiz_question_contains_contracts import Test_rs_quiz_question_contains_contracts

from services.quiz.operations.tests.test_questionChoices_operations import Test_questionChoices_operations
from services.quiz.operations.tests.test_questions_operations import Test_questions_operations
from services.quiz.operations.tests.test_quizzes_operations import Test_quizzes_operations
from services.quiz.operations.tests.test_rs_quiz_course_assigns_operations import Test_rs_quiz_course_assigns_operations
from services.quiz.operations.tests.test_rs_quiz_question_contains_operations import Test_rs_quiz_question_contains_operations


if __name__ == '__main__':
    unittest.main()
