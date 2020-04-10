import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest

from exceptions import ErrorWithCode

from models import db, User,Course,Student
from run_test import create_app
app = create_app()
app.app_context().push()
db.init_app(app)

from models import User,Course,Student
from services.core.operations.users_operations import encrypt
from services.core.operations.rs_student_course_enrols_operations import \
    initializeRsStudentCourseEnrol, courseMngReadOperation, courseMngCreateOperation, \
    courseClasslistReadOperation


class Test_rs_student_course_enrols_operations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def setUp(self):

        db.session.remove()
        db.drop_all()
        db.create_all()

        course = Course(index='cz3003')
        db.session.add(course)

        user = User(
            email='student@gmail.com',
            encrypted_password=encrypt('password'),
            name='std'
        )
        std = Student(user,"U1722")
        db.session.add(std)

        rs = initializeRsStudentCourseEnrol(1,'cz3003')
        db.session.add(rs)
        
        db.session.commit()


    def test_courseMngCreateOperation(self):

        with self.assertRaises(ErrorWithCode):
            courseMngCreateOperation("a@gmail.com",'cz3003')
            courseMngCreateOperation('student@gmail.com', "cz3007")
            courseMngCreateOperation('student@gmail.com', "cz3003")

        course = Course(index='cz3007')
        db.session.add(course)
        db.session.commit()
        self.assertIsNotNone(courseMngCreateOperation('student@gmail.com',"cz3007"))


    def test_courseMngReadOperation(self):

        with self.assertRaises(ErrorWithCode):
            courseMngReadOperation("student2@gmail.com")

        self.assertIsNotNone( courseMngReadOperation('student@gmail.com'))

    
    def test_courseClasslistReadOperation(self):

        self.assertRaises(ErrorWithCode, courseClasslistReadOperation, 'cz1003')
        self.assertEqual(len(courseClasslistReadOperation('cz3003')), 1)
        self.assertEqual(courseClasslistReadOperation('cz3003')[0].student_id, 1)


if __name__ == '__main__':
    unittest.main()
