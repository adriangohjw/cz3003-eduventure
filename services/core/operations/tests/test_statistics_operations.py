import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest

from exceptions import ErrorWithCode

from models import db
from run_test import create_app
app = create_app()
app.app_context().push()
db.init_app(app)

import datetime

from models import (
    User, Student, Staff, Topic, Lesson, Quiz, QuizAttempt, Question, Course,
    Rs_lesson_quiz_contain, Rs_quiz_course_assign, Rs_quiz_question_contain, Rs_student_course_enrol
)
from services.core.operations.users_operations import encrypt
from services.core.operations.statistics_operations import (
    statReadOperation, 
    lessonCompletedReadOperation, 
    leaderboardReadOperation, 
    studentScoreReadOperation,
    courseScoreReadOperation, 
    activityReadOperation
)


"""
This is a TestCase object to test the functions in statistics_operations.py
"""
class Test_statistics_operations(unittest.TestCase):
    
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

    # test the function statReadOperation
    def test_statReadOperation(self):

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(
            statReadOperation(),
            {
                "stats": [
                    {
                    "course_index": "cz1005",
                    "quizzes": [
                        {
                        "25th_percentile": 0.0,
                        "75th_percentile": 0.0,
                        "95th_percentile": 0.0,
                        "attempts": [
                            0
                        ],
                        "avg_score": 0,
                        "id": 1,
                        "max_score": 0,
                        "min_score": 0,
                        "name": "quiz_1",
                        "stdev": None
                        },
                        {
                        "25th_percentile": None,
                        "75th_percentile": None,
                        "95th_percentile": None,
                        "attempts": [],
                        "avg_score": None,
                        "id": 2,
                        "max_score": None,
                        "min_score": None,
                        "name": "quiz_2",
                        "stdev": None
                        },
                        {
                        "25th_percentile": 2.25,
                        "75th_percentile": 2.75,
                        "95th_percentile": 2.95,
                        "attempts": [
                            3,
                            2
                        ],
                        "avg_score": 2.5,
                        "id": 3,
                        "max_score": 3,
                        "min_score": 2,
                        "name": "quiz_3",
                        "stdev": 0.71
                        }
                    ]
                    }
                ]
            }
        )

    # test the function lessonCompletedReadOperation
    def test_lessonCompletedReadOperation(self):

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(
            lessonCompletedReadOperation(),
            {
                "courses": [
                    {
                        "course_index": "cz1005",
                        "progress": [
                            {
                                "lessons": [
                                    {
                                        "count_completed": 0,
                                        "lesson_id": 1,
                                        "lesson_name": "lesson_1"
                                    },
                                    {
                                        "count_completed": 0,
                                        "lesson_id": 2,
                                        "lesson_name": "lesson_2"
                                    },
                                    {
                                        "count_completed": 1,
                                        "lesson_id": 3,
                                        "lesson_name": "lesson_3"
                                    }
                                ],
                                "topic_id": 1,
                                "topic_name": "topic_1"
                            },
                            {
                                "lessons": [
                                    {
                                        "count_completed": 0,
                                        "lesson_id": 1,
                                        "lesson_name": "lesson_4"
                                    }
                                ],
                                "topic_id": 2,
                                "topic_name": "topic_2"
                            }
                        ]
                    },
                    {
                        "course_index": "all",
                        "progress": [
                            {
                                "lessons": [
                                    {
                                        "count_completed": 0,
                                        "lesson_id": 1,
                                        "lesson_name": "lesson_1"
                                    },
                                    {
                                        "count_completed": 0,
                                        "lesson_id": 2,
                                        "lesson_name": "lesson_2"
                                    },
                                    {
                                        "count_completed": 1,
                                        "lesson_id": 3,
                                        "lesson_name": "lesson_3"
                                    }
                                ],
                                "topic_id": 1,
                                "topic_name": "topic_1"
                            },
                            {
                                "lessons": [
                                    {
                                        "count_completed": 0,
                                        "lesson_id": 1,
                                        "lesson_name": "lesson_4"
                                    }
                                ],
                                "topic_id": 2,
                                "topic_name": "topic_2"
                            }
                        ]
                    }
                ]
            }
        )

    # test the function leaderboardReadOperation
    def test_leaderboardReadOperation(self):

        # check that when successful, result returned by function is correct (1)
        print('--- check that when successful, result returned by function is correct (1)')
        self.assertEqual(
            leaderboardReadOperation(None),
            {
                "scores": [
                    {
                    "id": 1,
                    "matriculation_num": "U00000000A",
                    "name": "student_1",
                    "score": 3
                    },
                    {
                    "id": 2,
                    "matriculation_num": "U00000000B",
                    "name": "student_2",
                    "score": 2
                    }
                ]
            }
        )

        # check that when successful, result returned by function is correct (2)
        print('--- check that when successful, result returned by function is correct (2)')
        self.assertEqual(
            leaderboardReadOperation(1),
            {
                "scores": [
                    {
                    "id": 1,
                    "matriculation_num": "U00000000A",
                    "name": "student_1",
                    "score": 3
                    }
                ]
            }
        )

    # test the function studentScoreReadOperation
    def test_studentScoreReadOperation(self):

        # check that when successful, result returned by function is correct (1)
        print('--- check that when successful, result returned by function is correct (1)')
        self.assertEqual(
            studentScoreReadOperation(None),
            {
                "students": [
                    {
                    "id": 1,
                    "name": "student_1",
                    "quizzes": [
                        {
                        "id": 1,
                        "name": "quiz_1",
                        "score": 0
                        },
                        {
                        "id": 3,
                        "name": "quiz_3",
                        "score": 3
                        }
                    ]
                    },
                    {
                    "id": 2,
                    "name": "student_2",
                    "quizzes": [
                        {
                        "id": 3,
                        "name": "quiz_3",
                        "score": 2
                        }
                    ]
                    }
                ]
            }
        )

        # check that when successful, result returned by function is correct (2)
        print('--- check that when successful, result returned by function is correct (2)')
        self.assertEqual(
            studentScoreReadOperation(1),
            {
                "students": [
                    {
                    "id": 1,
                    "name": "student_1",
                    "quizzes": [
                        {
                        "id": 1,
                        "name": "quiz_1",
                        "score": 0
                        },
                        {
                        "id": 3,
                        "name": "quiz_3",
                        "score": 3
                        }
                    ]
                    }
                ]
            }
        )

    # test the function courseScoreReadOperation
    def test_courseScoreReadOperation(self):

        # check that when successful, result returned by function is correct (1)
        print('--- check that when successful, result returned by function is correct (1)')
        self.assertEqual(
            courseScoreReadOperation(None),
            {
                "courses": [
                    {
                        "course_index": "cz1005",
                        "scores": {
                            "0-10": 1,
                            "11-20": 0,
                            "21-30": 0,
                            "31-40": 0,
                            "41-50": 0,
                            "51-60": 0,
                            "61-70": 1,
                            "71-80": 0,
                            "81-90": 0,
                            "91-100": 1
                        }
                    },
                    {
                        "course_index": "all",
                        "scores": {
                            "0-10": 1,
                            "11-20": 0,
                            "21-30": 0,
                            "31-40": 0,
                            "41-50": 0,
                            "51-60": 0,
                            "61-70": 1,
                            "71-80": 0,
                            "81-90": 0,
                            "91-100": 1
                        }
                    }
                ]
            }   
        )

        # check that when successful, result returned by function is correct (2)
        print('--- check that when successful, result returned by function is correct (2)')
        self.assertEqual(
            courseScoreReadOperation('cz1005'),
            {
                "courses": [
                    {
                        "course_index": "cz1005",
                        "scores": {
                            "0-10": 1,
                            "11-20": 0,
                            "21-30": 0,
                            "31-40": 0,
                            "41-50": 0,
                            "51-60": 0,
                            "61-70": 1,
                            "71-80": 0,
                            "81-90": 0,
                            "91-100": 1
                        }
                    }
                ]
            }   
        )

        # check that when successful, result returned by function is correct (3)
        print('--- check that when successful, result returned by function is correct (3)')
        self.assertEqual(
            courseScoreReadOperation('cz1003'),
            {
                "courses": []
            }   
        )

    # test the function activityReadOperation
    def test_activityReadOperation(self):

        date_today = datetime.date.today()
        date_today_str = date_today.strftime('%Y-%m-%d')
        
        # check that when successful, result returned by function is correct (1)
        print('--- check that when successful, result returned by function is correct (1)')
        self.assertEqual(
            activityReadOperation(date_today, date_today, 1),
            {
                "attempts": [
                    {
                    date_today_str: 2
                    }
                ]
            }
        )

        # check that when successful, result returned by function is correct (2)
        print('--- check that when successful, result returned by function is correct (2)')
        self.assertEqual(
            activityReadOperation(
                date_today + datetime.timedelta(days=10), 
                date_today + datetime.timedelta(days=10), 
                1),
            {
                "attempts": []
            }
        )
        

if __name__ == '__main__':
    unittest.main(verbosity=2)
