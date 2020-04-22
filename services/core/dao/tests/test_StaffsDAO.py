import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from models import db, User,Staff
from run_test import create_app
from services.core.operations.users_operations import encrypt

app = create_app()
app.app_context().push()
db.init_app(app)

from services.core.dao.StaffsDAO import (
    staffCreate,
    staffRead,
    staffUpdate
)


"""
This is a TestCase object to test the functions in StaffsDAO.py
"""
class Test_StaffsDAO(unittest.TestCase):
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

    # test the function staffCreate
    def test_staffCreate(self):

        # create a new Staff object
        user = User(
            email='staff@gmail.com',
            encrypted_password=encrypt('password'),
            name='staff'
        )
        stf = Staff(user=user)

        # add Staff object to the database
        staffCreate(stf)

        # retrieve all records from the table 'staffs'
        stf_list = Staff.query.all()

        # check that the number of record added is correct
        print('--- check that the number of record added is correct')
        self.assertEqual(1, len(stf_list))

        # check that the value(s) of the Staff object added is correct
        print('--- check that the value(s) of the Staff object added is correct')
        self.assertEqual(stf_list[0].email,'staff@gmail.com')

    # test the function staffRead
    def test_staffRead(self):

        # create a new Staff object and add it to the database
        user = User(
            email='staff@gmail.com',
            encrypted_password=encrypt('password'),
            name='staff'
        )
        stf = Staff(user=user)
        db.session.add(stf)
        db.session.commit()

        # check that the record retrieved is correct (using col='email')
        print('--- check that the record retrieved is correct (using col=\'email\')')
        self.assertTrue(staffRead('email','staff@gmail.com'))

        # check that the record retrieved is correct (using col='id')
        print('--- check that the record retrieved is correct (using col=\'id\')')
        self.assertTrue(staffRead('id',1))

    # test the function staffUpdate
    def test_staffUpdate(self):

        # create a new Staff object and add it to the database
        user = User(
            email='staff@gmail.com',
            encrypted_password=encrypt('password'),
            name='staff'
        )
        stf = Staff(user=user)
        db.session.add(stf)
        db.session.commit()

        # update value of Staff object
        stf.name = 'Justin'
        staffUpdate()

        # fetch updated Staff object from the database
        stf = Staff.query.filter_by(email='staff@gmail.com').first()

        # check if value of Staff object has been updated
        print('--- check if value of Staff object has been updated')
        self.assertEqual('Justin', stf.name)


if __name__ == '__main__':
    unittest.main(verbosity=2)
