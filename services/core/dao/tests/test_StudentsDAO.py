import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from models import db,User,Student
from run_test import create_app
from services.core.operations.users_operations import encrypt

app = create_app()
app.app_context().push()
db.init_app(app)

from services.core.dao.StudentsDAO import (
    studentCreate,
    studentRead,
    studentUpdate
)


"""
This is a TestCase object to test the functions in StudentsDAO.py
"""
class Test_StudentsDAO(unittest.TestCase):
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

    # test the function studentCreate
    def test_studentCreate(self):

        # create a new Student object
        user = User(
            email='student@gmail.com',
            encrypted_password=encrypt('password'),
            name='std'
        )
        std = Student(user=user,matriculation_number="U1722")

        # add Student object to the database
        studentCreate(std)

        # retrieve all records from the table 'students'
        std_list = Student.query.all()

        # check that the number of record added is correct
        print('--- check that the number of record added is correct')
        self.assertEqual(1, len(std_list))

        # check that the value(s) of the Student object added is correct
        print('--- check that the value(s) of the Student object added is correct')
        self.assertEqual(std_list[0].email,'student@gmail.com')

    # test the function studentRead
    def test_studentRead(self):

        # create a new Student object and add it to the database
        user = User(
            email='student@gmail.com',
            encrypted_password=encrypt('password'),
            name='std'
        )
        std = Student(user=user, matriculation_number="U1722")
        db.session.add(std)
        db.session.commit()

        # check that the record retrieved is correct (using col='email')
        print('--- check that the record retrieved is correct (using col=\'email\')')
        self.assertTrue(studentRead('email','student@gmail.com'))

        # check that the record retrieved is correct (using col='id')
        print('--- check that the record retrieved is correct (using col=\'id\')')
        self.assertTrue(studentRead('id',1))

    # test the function studentUpdate
    def test_studentUpdate(self):
        
        # create a new Student object and add it to the database
        user = User(
            email='student@gmail.com',
            encrypted_password=encrypt('password'),
            name='std'
        )
        std = Student(user=user, matriculation_number="U1722")
        db.session.add(std)
        db.session.commit()

        # update value of Student object
        std.name = 'Justin'
        studentUpdate()

        # fetch updated User object from the database
        std = Student.query.filter_by(email='student@gmail.com').first()

        # check if value of Student object has been updated
        print('--- check if value of Student object has been updated')
        self.assertEqual('Justin', std.name)


if __name__ == '__main__':
    unittest.main(verbosity=2)
