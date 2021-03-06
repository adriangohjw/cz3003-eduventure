import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest

from models import db
from run_test import create_app
app = create_app()
app.app_context().push()
db.init_app(app)

from models import \
    User, Student, Staff, Topic, Lesson, Quiz, QuizAttempt, QuestionAttempt, Question, QuestionChoice, Course, Challenge, \
    Rs_lesson_quiz_contain, Rs_quiz_course_assign, Rs_quiz_question_contain, Rs_student_course_enrol, \
    Rs_staff_course_teach
from services.core.operations.users_operations import encrypt

import json 


def res_to_dict(response):
    dict_str = response.data.decode("UTF-8")
    mydata = json.loads(dict_str)
    return mydata


class Test_BaseCase(unittest.TestCase):

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

        self.app = app.test_client()

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
        question_1 = Question(1, 1, 'description_1')
        db.session.add(question_1)
        question_2 = Question(1, 1, 'description_2')
        db.session.add(question_2)
        question_3 = Question(1, 3, 'description_3')
        db.session.add(question_3)
        question_4 = Question(1, 3, 'description_4')
        db.session.add(question_4)
        question_5 = Question(1, 3, 'description_5')
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

        # add attempts to questions
        question_attempt_1 = QuestionAttempt(1, 1, True, 10)
        db.session.add(question_attempt_1)
        question_attempt_2 = QuestionAttempt(1, 1, False, 20)
        db.session.add(question_attempt_2)
        question_attempt_3 = QuestionAttempt(1, 2, True, 30)
        db.session.add(question_attempt_3)
        question_attempt_4 = QuestionAttempt(1, 3, False, 40)
        db.session.add(question_attempt_4)

        # add question choices to questions 
        qc_1 = QuestionChoice(1, 1, 'choice_1', True)
        db.session.add(qc_1)
        qc_2 = QuestionChoice(1, 2, 'choice_2', True)
        db.session.add(qc_2)
        qc_3 = QuestionChoice(1, 3, 'choice_3', True)
        db.session.add(qc_3)

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

        # make staff teach course
        teach_1 = Rs_staff_course_teach(3, 'cz1005')
        db.session.add(teach_1)

        # adding quizzes to courses
        Rs_quiz_course_assign_1 = Rs_quiz_course_assign(1, 'cz1005')
        db.session.add(Rs_quiz_course_assign_1)
        Rs_quiz_course_assign_2 = Rs_quiz_course_assign(2, 'cz1005')
        db.session.add(Rs_quiz_course_assign_2)
        Rs_quiz_course_assign_3 = Rs_quiz_course_assign(3, 'cz1005')
        db.session.add(Rs_quiz_course_assign_3)

        # adding challenges
        challenge_1 = Challenge(1, 2, 1)
        db.session.add(challenge_1)
        challenge_2 = Challenge(1, 2, 2)
        db.session.add(challenge_2)
        challenge_3 = Challenge(2, 1, 1)
        db.session.add(challenge_3)

        db.session.commit()
