import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest

from models import db
from run_test import create_app
app = create_app()
app.app_context().push()
db.init_app(app)

from models import Quiz, Staff, User, Topic,Lesson, Question,  Student, Course, Rs_student_course_enrol
from services.core.operations.users_operations import encrypt
from services.core.dao.RsStudentCourseEnrolDAO import \
    rsStudentCourseEnrolCreate, rsStudentCourseEnrolRead, rsCourseEnrolRead


class Test_RsStudentCourseEnrolDAO(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    
    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()

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

        topic = Topic(name='seng')
        db.session.add(topic)

        lesson = Lesson(topic_id='1', id='3', name='se', content='test')
        db.session.add(lesson)

        qn = Question('1', '3', 'easy')
        db.session.add(qn)

        qz = Quiz(2, 'quiz', True, '2020-03-21', '2020-03-22')  # staff id is 2 here, as it uses the fk of users table
        db.session.add(qz)

        course = Course(index='cz3003')
        db.session.add(course)

        db.session.commit()


    def test_rsStudentCourseEnrolCreate(self):

        rs = Rs_student_course_enrol(1,'cz3003')

        rsStudentCourseEnrolCreate(rs)

        rs_list = Rs_student_course_enrol.query.all()

        self.assertEqual(1, len(rs_list))
        self.assertEqual(rs_list[0].course_index,'cz3003')


    def test_rsStudentCourseEnrolRead(self):

        self.assertIsNone(rsStudentCourseEnrolRead(student_id=1,course_index='cz3003'))

    
    def test_rsCourseEnrolRead(self):

        self.assertEqual(len(rsCourseEnrolRead('cz3003')), 0)

        rs = Rs_student_course_enrol(1,'cz3003')
        db.session.add(rs)
        db.session.commit()

        self.assertEqual(len(rsCourseEnrolRead('cz3003')), 1)


if __name__ == '__main__':
    unittest.main()
