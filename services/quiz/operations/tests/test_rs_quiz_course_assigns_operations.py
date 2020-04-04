import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from services.quiz.operations.rs_quiz_course_assigns_operations import initializeRsQuizCourseAssign,courseMngReadOperation,courseMngCreateOperation
from exceptions import ErrorWithCode

from models import db, User,Staff,Quiz,Course
from run_test import create_app
from services.core.operations.users_operations import encrypt

app = create_app()
app.app_context().push()
db.init_app(app)


class Test_rs_quiz_course_assigns_operations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()
        course = Course(index='cz3003')
        db.session.add(course)
        db.session.commit()
        user = User(
            email='staff@gmail.com',
            encrypted_password=encrypt('password'),
            name='staff'
        )
        staff = Staff(user)
        db.session.add(staff)
        qz = Quiz(1, 'quiz', True, '2020-03-21', '2020-03-22')  # staff id is 2 here, as it uses the fk of users table
        db.session.add(qz)
        db.session.commit()
        rs = initializeRsQuizCourseAssign(1,'cz3003')
        db.session.add(rs)
        db.session.commit()

    def test_courseMngCreateOperation(self):
        with self.assertRaises(ErrorWithCode):
            courseMngCreateOperation(1,"cz3007")
            courseMngCreateOperation(2, "cz3007")
            courseMngCreateOperation(1, "cz3003")

        course = Course(index='cz3007')
        db.session.add(course)
        db.session.commit()
        self.assertIsNotNone(courseMngCreateOperation(1,"cz3007"))#same quiz can be to different courses?

    def test_courseMngReadOperation(self):
        with self.assertRaises(ErrorWithCode):
            courseMngReadOperation(2)

        self.assertIsNotNone( courseMngReadOperation(1))

if __name__ == '__main__':
    unittest.main()
