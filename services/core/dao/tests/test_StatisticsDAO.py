import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest

from models import db
from run_test import create_app
app = create_app()
app.app_context().push()
db.init_app(app)

from models import (
    User, Student, Staff, Topic, Lesson, Quiz, QuizAttempt, Question, Course,\
    Rs_lesson_quiz_contain, Rs_quiz_course_assign, Rs_quiz_question_contain, Rs_student_course_enrol
)
from services.core.operations.users_operations import encrypt
from services.core.dao.StatisticsDAO import (
    statRead, 
    lessonCompletedRead, 
    leaderboardRead, 
    studentScoreRead, 
    courseScoreRead, 
    activityRead
)

import datetime


"""
This is a TestCase object to test the functions in StatisticsDAO.py
"""
class Test_StatisticsDAO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    # this will run before every test
    # it will ensure that every test start with a fresh database
    def setUp(self):
        print('\r')
        # drop all tables in the database
        db.session.remove()
        db.drop_all()
        # crete all tables in the database
        db.create_all()

        self.maxDiff = None

        # adding students
        user_1 = User('student_1@gmail.com', encrypt('password'), 'student_1')
        student_1 = Student(user_1, 'U00000000A')
        db.session.add(student_1)
        user_2 = User('student_2gmail.com', encrypt('password'), 'student_2')
        student_2 = Student(user_2, 'U00000000B')
        db.session.add(student_2)

        # adding staff
        user_3 = User('staff_1@gmail.com', encrypt('password'), 'staff_1')
        staff_1 = Staff(user_3)
        db.session.add(staff_1)

        # adding topics
        topic_1 = Topic(name='topic_1')
        db.session.add(topic_1)
        topic_2 = Topic(name='topic_2')
        db.session.add(topic_2)

        # adding lessons
        lesson_1 = Lesson(topic_id=1, id=1, name='lesson_1', content='content')
        db.session.add(lesson_1)
        lesson_2 = Lesson(topic_id=1, id=2, name='lesson_2', content='content')
        db.session.add(lesson_2)
        lesson_3 = Lesson(topic_id=1, id=3, name='lesson_3', content='content')
        db.session.add(lesson_3)
        lesson_4 = Lesson(topic_id=2, id=1, name='lesson_4', content='content')
        db.session.add(lesson_4)

        # adding quizzes
        quiz_1 = Quiz(3, 'quiz_1', True, '2020-03-30', '2020-03-31')
        db.session.add(quiz_1)
        quiz_2 = Quiz(3, 'quiz_2', True, '2020-03-30', '2020-03-31')
        db.session.add(quiz_2)
        quiz_3 = Quiz(3, 'quiz_3', True, '2020-03-30', '2020-03-31')
        db.session.add(quiz_3)

        # adding questions
        question_1 = Question(1, 1, 'description')
        db.session.add(question_1)
        question_2 = Question(1, 1, 'description')
        db.session.add(question_2)
        question_3 = Question(1, 3, 'description')
        db.session.add(question_3)
        question_4 = Question(1, 3, 'description')
        db.session.add(question_4)
        question_5 = Question(1, 3, 'description')
        db.session.add(question_5)

        # assign questions to quiz
        rs_1 = Rs_quiz_question_contain(1, 1)
        db.session.add(rs_1)
        rs_2 = Rs_quiz_question_contain(3, 3)
        db.session.add(rs_2)
        rs_3 = Rs_quiz_question_contain(3, 4)
        db.session.add(rs_3)
        rs_4 = Rs_quiz_question_contain(3, 5)
        db.session.add(rs_4)

        # adding quiz attempts
        quiz_attempt_1 = QuizAttempt(1, 1, 0)
        db.session.add(quiz_attempt_1)
        quiz_attempt_2 = QuizAttempt(2, 3, 2)
        db.session.add(quiz_attempt_2)
        quiz_attempt_3 = QuizAttempt(1, 3, 3)
        db.session.add(quiz_attempt_3)

        # adding quizzes to lessons
        rs_lesson_quiz_contain_1 = Rs_lesson_quiz_contain(1, 1, 1)
        db.session.add(rs_lesson_quiz_contain_1)
        rs_lesson_quiz_contain_2 = Rs_lesson_quiz_contain(1, 1, 2)
        db.session.add(rs_lesson_quiz_contain_2)
        rs_lesson_quiz_contain_3 = Rs_lesson_quiz_contain(1, 3, 3)
        db.session.add(rs_lesson_quiz_contain_3)

        # adding courses
        course = Course('cz1005')
        db.session.add(course)

        # enrol students into courses
        enrol_1 = Rs_student_course_enrol(1, 'cz1005')
        db.session.add(enrol_1)
        enrol_2 = Rs_student_course_enrol(2, 'cz1005')
        db.session.add(enrol_2)

        # adding quizzes to courses
        Rs_quiz_course_assign_1 = Rs_quiz_course_assign(1, 'cz1005')
        db.session.add(Rs_quiz_course_assign_1)
        Rs_quiz_course_assign_2 = Rs_quiz_course_assign(2, 'cz1005')
        db.session.add(Rs_quiz_course_assign_2)
        Rs_quiz_course_assign_3 = Rs_quiz_course_assign(3, 'cz1005')
        db.session.add(Rs_quiz_course_assign_3)

        db.session.commit()

    # test the function statRead
    def test_statRead(self):

        # check res returned by func is correct
        print('--- test if result returned is correct')
        self.assertEqual(
            statRead(),
            [
                ('cz1005', 1, 'quiz_1', 1, 0),
                ('cz1005', 1, 'quiz_1', 2, None),
                ('cz1005', 2, 'quiz_2', 1, None),
                ('cz1005', 2, 'quiz_2', 2, None),
                ('cz1005', 3, 'quiz_3', 1, 3),
                ('cz1005', 3, 'quiz_3', 2, 2)
            ]
        )

    # test the function 
    def test_lessonCompletedRead(self):

        # check res returned by func is correct
        print('--- test if result returned is correct')
        self.assertEqual(
            lessonCompletedRead(),
            [
                (1, 'topic_1', 1, 'lesson_1', 1, 'quiz_1', 'cz1005', 1, 0, 1),
                (1, 'topic_1', 1, 'lesson_1', 2, 'quiz_2', None, None, None, 0), 
                (1, 'topic_1', 2, 'lesson_2', None, None, None, None, None, 0), 
                (1, 'topic_1', 3, 'lesson_3', 3, 'quiz_3', 'cz1005', 1, 3, 3), 
                (1, 'topic_1', 3, 'lesson_3', 3, 'quiz_3', 'cz1005', 2, 2, 3), 
                (2, 'topic_2', 1, 'lesson_4', None, None, None, None, None, 0)
            ]
        )

    # test the function 
    def test_leaderboardRead(self):

        # check res returned by func is correct
        print('--- test if result returned is correct')
        self.assertEqual(
            leaderboardRead(),
            [
                (1, 'student_1', 'U00000000A', 1, 0),
                (1, 'student_1', 'U00000000A', 3, 3), 
                (2, 'student_2', 'U00000000B', 3, 2)
            ]
        )

    # test the function 
    def test_studentScoreRead(self):

        # check res returned by func is correct
        print('--- test if result returned is correct')
        self.assertEqual(
            studentScoreRead(),
            [
                (1, 'student_1', 1, 'quiz_1', 0),
                (1, 'student_1', 3, 'quiz_3', 3), 
                (2, 'student_2', 3, 'quiz_3', 2)
            ]
        )

    # test the function 
    def test_courseScoreRead(self):

        # check res returned by func is correct
        print('--- test if result returned is correct')
        self.assertEqual(
            courseScoreRead(),
            [
                ('cz1005', 1, 1, 0),
                ('cz1005', 1, 3, 100),
                ('cz1005', 2, 3, 67),
            ]
        )

    # test the function 
    def test_activityRead(self):

        # Manually set date as object creation uses datetime.now()
        # So that test result will be independent on date that test is being ran
        date_today = datetime.date.today()
        date_today_str = date_today.strftime('%Y-%m-%d')

        # check res returned by func is correct (1)
        print('--- test if result returned is correct (1)')
        self.assertEqual(
            activityRead(date_today, date_today, 1),
            [
                (datetime.date(date_today.year, date_today.month, date_today.day), 1),
                (datetime.date(date_today.year, date_today.month, date_today.day), 3)
            ]
        )

        # check res returned by func is correct (2)
        print('--- test if result returned is correct (2)')
        self.assertEqual(
            activityRead(
                date_today + datetime.timedelta(days=10), 
                date_today + datetime.timedelta(days=10), 
                1
            ),
            []
        )


if __name__ == '__main__':
    unittest.main(verbosity=2)
