import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from services.core.operations.rs_staff_course_teaches_operations import (
    initializeRsStaffCourseTeach,
    courseMngCreateOperation,
    courseMngReadOperation
)
from exceptions import ErrorWithCode

from models import (
    db, User, Staff, Quiz, Course, Rs_staff_course_teach
)
from run_test import create_app
from services.core.operations.users_operations import encrypt

app = create_app()
app.app_context().push()
db.init_app(app)


"""
This is a TestCase object to test the functions in rs_staff_course_teaches_operations.py
"""
class Test_rs_staff_course_teaches_operations(unittest.TestCase):
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
            email='staff@gmail.com',
            encrypted_password=encrypt('password'),
            name='staff'
        )
        staff = Staff(user)
        db.session.add(staff)

        # adding RsStaffCourseTeach 
        rs = initializeRsStaffCourseTeach(1,'cz3003')
        db.session.add(rs)
        db.session.commit()

    # test the function courseMngCreateOperation
    def test_courseMngCreateOperation(self):

        # check that error raised when record (student) does not exist
        print('--- check that error raised when record (staff) does not exist')
        with self.assertRaises(ErrorWithCode):
            courseMngCreateOperation("a@gmail.com",'cz3003')

        # check that error raised when record (course) does not exist
        print('--- check that error raised when record (course) does not exist')
        with self.assertRaises(ErrorWithCode):
            courseMngCreateOperation('staff@gmail.com', "cz3007")

        # check that error raised when record already exist
        print('--- check that error raised when record already exist')
        with self.assertRaises(ErrorWithCode):
            courseMngCreateOperation('staff@gmail.com', "cz3003")

        # adding courses
        course = Course(index='cz3007')
        db.session.add(course)
        db.session.commit()

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(courseMngCreateOperation('staff@gmail.com',"cz3007")), Rs_staff_course_teach)

    # test the function courseMngReadOperation
    def test_courseMngReadOperation(self):

        # check that error raised when record does not exist
        print('--- check that error raised when record does not exist')
        with self.assertRaises(ErrorWithCode):
            courseMngReadOperation("staff2@gmail.com")

        # check that when successful, result returned by function is of the correct type
        print('--- check that when successful, result returned by function is of the correct type')
        self.assertEqual(type(courseMngReadOperation('staff@gmail.com')), Staff)

        # check that when successful, result returned by function is correct
        print('--- check that when successful, result returned by function is correct')
        self.assertEqual(courseMngReadOperation('staff@gmail.com').name, 'staff')

if __name__ == '__main__':
    unittest.main(verbosity=2)
