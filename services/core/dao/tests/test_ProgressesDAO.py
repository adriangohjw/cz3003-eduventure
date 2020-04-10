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
    User, Student, Staff, Topic, Lesson, Quiz, Question, QuizAttempt, \
    Rs_lesson_quiz_contain, Rs_quiz_question_contain
from services.core.operations.users_operations import encrypt
from services.core.dao.ProgressesDAO import progressRead


class Test_ProgressesDAO(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()

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

        # adding questions to quizzes
        rs_quiz_question_contain_1 = Rs_quiz_question_contain(1, 1)
        db.session.add(rs_quiz_question_contain_1)
        rs_quiz_question_contain_2 = Rs_quiz_question_contain(3, 3)
        db.session.add(rs_quiz_question_contain_2)
        rs_quiz_question_contain_3 = Rs_quiz_question_contain(3, 4)
        db.session.add(rs_quiz_question_contain_3)
        rs_quiz_question_contain_4 = Rs_quiz_question_contain(3, 5)
        db.session.add(rs_quiz_question_contain_4)

        db.session.commit()


    def test_progressRead(self):

        self.assertEqual(
            progressRead(1),
            [
                (1, 'topic_1', 1, 'lesson_1', 1, 'quiz_1', 1, 0, 1),
                (1, 'topic_1', 1, 'lesson_1', 2, 'quiz_2', None, 0, 0), 
                (1, 'topic_1', 2, 'lesson_2', None, None, None, 0, 0), 
                (1, 'topic_1', 3, 'lesson_3', 3, 'quiz_3', 1, 3, 3), 
                (2, 'topic_2', 1, 'lesson_4', None, None, None, 0, 0)
            ]
        )


if __name__ == '__main__':
    unittest.main()
