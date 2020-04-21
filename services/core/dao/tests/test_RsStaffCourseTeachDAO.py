import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from models import (
    db, QuizAttempt, Quiz, Staff, User,Topic,Lesson, Question,  Student, Course,Rs_staff_course_teach
)
from run_test import create_app
from services.core.operations.users_operations import encrypt

app = create_app()
app.app_context().push()
db.init_app(app)

from services.core.dao.RsStaffCourseTeachDAO import (
    rsStaffCourseTeachCreate,
    rsStaffCourseTeachRead
)


"""
This is a TestCase object to test the functions in RsStaffCourseTeachDAO.py
"""
class Test_RsStaffCourseTeachDAO(unittest.TestCase):
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
        
        # adding users
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

        # adding topics
        topic = Topic(name='seng')
        db.session.add(topic)

        # adding lessons
        lesson = Lesson(topic_id='1', id='3', name='se', content='test')
        db.session.add(lesson)

        # adding questions
        qn = Question('1', '3', 'easy')
        db.session.add(qn)

        # adding quizzes
        qz = Quiz(2, 'quiz', True, '2020-03-21', '2020-03-22')  # staff id is 2 here, as it uses the fk of users table
        db.session.add(qz)

        # adding courses
        course = Course(index='cz3003')
        db.session.add(course)

        db.session.commit()

    # test the function rsStaffCourseTeachCreate
    def test_rsStaffCourseTeachCreate(self):

        # create a new relationship object
        rs = Rs_staff_course_teach(2,'cz3003')

        # add relationship object to the database
        rsStaffCourseTeachCreate(rs)

        # retrieve all records from the table
        rs_list = Rs_staff_course_teach.query.all()

        # check that the number of record added is correct
        print('--- check that the number of record added is correct')
        self.assertEqual(1, len(rs_list))

        # check that the value(s) of the relationship object added is correct
        print('--- check that the value(s) of the relationship object added is correct')
        self.assertEqual(rs_list[0].course_index,'cz3003')

    # test the function rsStaffCourseTeachRead
    def test_rsStaffCourseTeachRead(self):

        # create a new relationship object and add to the database
        rs = Rs_staff_course_teach(2,'cz3003') 
        db.session.add(rs)
        db.session.commit()

        # check the number of record retrived is correct
        print('--- check the number of record retrived is correct')
        self.assertEqual(rsStaffCourseTeachRead(staff_id=2,course_index='cz3003').staff_id, 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
