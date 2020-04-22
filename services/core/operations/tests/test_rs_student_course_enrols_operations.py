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

from models import (
    User, Course, Student, Rs_student_course_enrol
)
from services.core.operations.users_operations import encrypt
from services.core.operations.rs_student_course_enrols_operations import (
    initializeRsStudentCourseEnrol, 
    courseMngReadOperation, 
    courseMngCreateOperation, 
    courseClasslistReadOperation
)


"""
This is a TestCase object to test the functions in rs_student_course_enrols_operations.py
"""
class Test_rs_student_course_enrols_operations(unittest.TestCase):
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

        # adding courses
        course = Course(index='cz3003')
        db.session.add(course)

        # adding users
        user = User(
            email='student@gmail.com',
            encrypted_password=encrypt('password'),
            name='std'
        )
        std = Student(user,"U1722")
        db.session.add(std)

        # adding RsStudentCourseEnrol
        rs = initializeRsStudentCourseEnrol(1,'cz3003')
        db.session.add(rs)
        
        db.session.commit()

    # test the function courseMngCreateOperation
    def test_courseMngCreateOperation(self):

        # check that error raised when record (student) does not exist
        print('--- check that error raised when record (student) does not exist')
        with self.assertRaises(ErrorWithCode):
            courseMngCreateOperation("a@gmail.com",'cz3003')

        # check that error raised when record (course) does not exist
        print('--- check that error raised when record (course) does not exist')
        with self.assertRaises(ErrorWithCode):
            courseMngCreateOperation('student@gmail.com', "cz3007")

        # check that error raised when record already exist
        print('--- check that error raised when record already exist')
        with self.assertRaises(ErrorWithCode):
            courseMngCreateOperation('student@gmail.com', "cz3003")

        # adding courses
        course = Course(index='cz3007')
        db.session.add(course)
        db.session.commit()

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(courseMngCreateOperation('student@gmail.com',"cz3007")), Rs_student_course_enrol)

    # test the function courseMngReadOperation
    def test_courseMngReadOperation(self):

        # check that error raised when record does not exist
        print('--- check that error raised when record does not exist')
        with self.assertRaises(ErrorWithCode):
            courseMngReadOperation("student2@gmail.com")

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(courseMngReadOperation('student@gmail.com')), Student)

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(courseMngReadOperation('student@gmail.com').name, 'std')

    # test the function courseClasslistReadOperation
    def test_courseClasslistReadOperation(self):
        
        # check that error raised when record does not exist
        print('--- check that error raised when record does not exist')
        self.assertRaises(ErrorWithCode, courseClasslistReadOperation, 'cz1003')

        # check that when successful, number of records returned by function is correct
        print('--- check that when successful, number of records returned by function is correct')
        self.assertEqual(len(courseClasslistReadOperation('cz3003')), 1)

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(courseClasslistReadOperation('cz3003')[0].student_id, 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
