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
    Quiz, Staff, User, Topic,Lesson, Question,  Student, Course, Rs_student_course_enrol
)
from services.core.operations.users_operations import encrypt
from services.core.dao.RsStudentCourseEnrolDAO import (
    rsStudentCourseEnrolCreate, 
    rsStudentCourseEnrolRead, 
    rsCourseEnrolRead
)
    

"""
This is a TestCase object to test the functions in RsStudentCourseEnrolDAO.py
"""
class Test_RsStudentCourseEnrolDAO(unittest.TestCase):
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

        # adding users to database
        user = User(
            email='john_d@gmail.com',
            encrypted_password=encrypt('password'),
            name='john_doe'
        )
        student = Student(user, 'U1722')
        db.session.add(student)

        user = User(
            email='staff@gmail.com',
            encrypted_password=encrypt('password'),
            name='staff'
        )
        staff = Staff(user)
        db.session.add(staff)

        # adding topics to database
        topic = Topic(name='seng')
        db.session.add(topic)

        # adding lessons to database
        lesson = Lesson(topic_id='1', id='3', name='se', content='test')
        db.session.add(lesson)

        # adding questions to database
        qn = Question('1', '3', 'easy')
        db.session.add(qn)

        # adding quizzes to database
        qz = Quiz(2, 'quiz', True, '2020-03-21', '2020-03-22')  # staff id is 2 here, as it uses the fk of users table
        db.session.add(qz)

        # adding courses to database
        course = Course(index='cz3003')
        db.session.add(course)

        db.session.commit()

    # test the function rsStudentCourseEnrolCreate
    def test_rsStudentCourseEnrolCreate(self):

        # create a new relationship object
        rs = Rs_student_course_enrol(1,'cz3003')

        # add relationship object to the database
        rsStudentCourseEnrolCreate(rs)

        # retrieve all records from the table
        rs_list = Rs_student_course_enrol.query.all()

        # check that the number of record added is correct
        print('--- check that the number of record added is correct')
        self.assertEqual(1, len(rs_list))

        # check that the value(s) of the relationship object added is correct
        print('--- check that the value(s) of the relationship object added is correct')
        self.assertEqual(rs_list[0].course_index,'cz3003')

    # test the function rsStudentCourseEnrolRead
    def test_rsStudentCourseEnrolRead(self):

        # create a new relationship object and add it to the database
        rs = Rs_student_course_enrol(1,'cz3003')
        db.session.add(rs)
        db.session.commit()

        # check that the record retrieved is correct
        print('--- check that the record retrieved is correct')
        self.assertEqual(rsStudentCourseEnrolRead(1, 'cz3003').student_id, 1)

    # test the function rsCourseEnrolRead
    def test_rsCourseEnrolRead(self):

        # create a new relationship object and add it to the database
        rs = Rs_student_course_enrol(1,'cz3003')
        db.session.add(rs)
        db.session.commit()

        # check the number of record retrived is correct
        print('--- check the number of record retrived is correct')
        self.assertEqual(len(rsCourseEnrolRead('cz3003')), 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
