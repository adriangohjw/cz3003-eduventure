import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from services.core.operations.rs_staff_course_teaches_operations import initializeRsStaffCourseTeach,courseMngCreateOperation,courseMngReadOperation
from exceptions import ErrorWithCode

from models import db, User,Staff,Quiz,Course
from run_test import create_app
from services.core.operations.users_operations import encrypt

app = create_app()
app.app_context().push()
db.init_app(app)


class Test_rs_staff_course_teaches_operations(unittest.TestCase):
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
        rs = initializeRsStaffCourseTeach(1,'cz3003')
        db.session.add(rs)
        db.session.commit()

    def test_courseMngCreateOperation(self):
        with self.assertRaises(ErrorWithCode):
            courseMngCreateOperation("a@gmail.com",'cz3003')
            courseMngCreateOperation('staff@gmail.com', "cz3007")
            courseMngCreateOperation('staff@gmail.com', "cz3003")

        course = Course(index='cz3007')
        db.session.add(course)
        db.session.commit()
        self.assertIsNotNone(courseMngCreateOperation('staff@gmail.com',"cz3007"))

    def test_courseMngReadOperation(self):
        with self.assertRaises(ErrorWithCode):
            courseMngReadOperation("staff2@gmail.com")

        self.assertIsNotNone( courseMngReadOperation('staff@gmail.com'))

if __name__ == '__main__':
    unittest.main()
