import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from models import db, QuizAttempt, Quiz, Staff, User,Topic,Lesson, Question,  Student, Course,Rs_staff_course_teach
from run_test import create_app
from services.core.operations.users_operations import encrypt

app = create_app()
app.app_context().push()
db.init_app(app)

from services.core.dao.RsStaffCourseTeachDAO import rsStaffCourseTeachCreate,rsStaffCourseTeachRead


class Test_RsStaffCourseTeachDAO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))
        db.session.remove()
        db.drop_all()
        db.create_all()
        user = User(
            email='john_d@gmail.com',
            encrypted_password=encrypt('password'),
            name='john_doe'
        )
        # db.session.add(user)
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



    def test_rsStaffCourseTeachCreate(self):
        rs = Rs_staff_course_teach(2,'cz3003')

        rsStaffCourseTeachCreate(rs)

        rs_list = Rs_staff_course_teach.query.all()

        self.assertEqual(1, len(rs_list))
        self.assertEqual(rs_list[0].course_index,'cz3003')

    def test_rsStaffCourseTeachRead(self):
        self.assertTrue(rsStaffCourseTeachRead(staff_id=2,course_index='cz3003'))


if __name__ == '__main__':
    unittest.main()
