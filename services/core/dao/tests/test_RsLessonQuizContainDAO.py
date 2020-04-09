import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest

from models import db
from run_test import create_app
app = create_app()
app.app_context().push()
db.init_app(app)

from models import Topic, Lesson, Quiz, User, Staff, Rs_lesson_quiz_contain
from services.core.operations.users_operations import encrypt
from services.core.dao.RsLessonQuizContainDAO import \
    rsLessonQuizContainCreate, rsLessonQuizContainRead, rsLessonQuizContainDelete


class Test_RsLessonQuizContainDAO(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()

        topic = Topic(name='seng')
        db.session.add(topic)

        lesson = Lesson(topic_id=1, id=1, name='se', content='test')
        db.session.add(lesson)

        user = User('staff@gmail.com', encrypt('password'), 'staff_name')
        staff = Staff(user)
        db.session.add(staff)

        quiz = Quiz(1, 'quiz_name', True, '2020-03-21', '2020-03-22')
        db.session.add(quiz)

        db.session.commit()

    
    def test_rsLessonQuizContainCreate(self):
        
        self.assertEqual(len(Rs_lesson_quiz_contain.query.all()), 0)

        rs = Rs_lesson_quiz_contain(1, 1, 1)
        rsLessonQuizContainCreate(rs)

        self.assertEqual(len(Rs_lesson_quiz_contain.query.all()), 1)


    def test_rsLessonQuizContainRead(self):

        self.assertEqual(len(rsLessonQuizContainRead(1, 1)), 0)

        rs = Rs_lesson_quiz_contain(1, 1, 1)
        db.session.add(rs)
        db.session.commit()
        
        self.assertEqual(len(rsLessonQuizContainRead(1, 1)), 1)
        self.assertEqual(rsLessonQuizContainRead(1, 1)[0].quiz_id, 1)

    
    def test_rsLessonDelete(self):

        rs = Rs_lesson_quiz_contain(1, 1, 1)
        db.session.add(rs)
        db.session.commit()

        self.assertEqual(len(rsLessonQuizContainRead(1, 1)), 1)

        rsLessonQuizContainDelete(1)

        self.assertEqual(len(rsLessonQuizContainRead(1, 1)), 0)
        

if __name__ == '__main__':
    unittest.main()
