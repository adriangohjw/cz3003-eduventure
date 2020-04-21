import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest 

from models import db, User
from run_test import create_app

app = create_app()
app.app_context().push()
db.init_app(app)

from services.core.operations.users_operations import (
    encrypt,
    authenticate
)
from services.core.dao.UsersDAO import (
    userRead, 
    userCreate, 
    userUpdate
)


"""
This is a TestCase object to test the functions in UsersDAO.py
"""
class Test_users_dao(unittest.TestCase):
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
        
    # test the function userRead
    def test_userRead(self):

        # create a new User object and add it to the database
        user = User(
            email = 'john_doe@gmail.com',
            encrypted_password=encrypt('password'),
            name = 'john_doe'
        )
        db.session.add(user)
        db.session.commit()

        # check that the record retrieved is correct (using col='email')
        print('--- check that the record retrieved is correct (using col=\'email\')')
        self.assertTrue(userRead(col='email', value='john_doe@gmail.com'))

        # check that the record retrieved is correct (using col='id')
        print('--- check that the record retrieved is correct (using col=\'id\')')
        self.assertTrue(userRead(col='id', value=1))

    # test the function userCreate
    def test_userCreate(self):

        # create a new User object
        user = User(
            email = 'john_doe@gmail.com',
            encrypted_password=encrypt('password'),
            name = 'john_doe'
        )

        # add User object to the database
        userCreate(user)

        # retrieve all records from the table 'users'
        user_list = User.query.all()

        # check that the number of record added is correct
        print('--- check that the number of record added is correct')
        self.assertEqual(1, len(user_list))

        # check that the value(s) of the User object added is correct
        print('--- check that the value(s) of the User object added is correct')
        self.assertEqual(user_list[0].email, 'john_doe@gmail.com')

    # test the function userUpdate
    def test_userUpdate(self):

        # create a new User object and add it to the database
        user = User(
            email = 'john_doe@gmail.com',
            encrypted_password=encrypt('password'),
            name = 'john_doe'
        )
        db.session.add(user)
        db.session.commit()

        # update value of User object
        password_original = user.encrypted_password
        user.encrypted_password = encrypt('password_new')
        userUpdate()

        # fetch updated User object from the database
        user = User.query.filter_by(email='john_doe@gmail.com').first()

        # check if value of User object has been updated
        print('--- check if value of User object has been updated')
        self.assertTrue(authenticate('password_new', user.encrypted_password))
        

if __name__ == '__main__':
    unittest.main(verbosity=2)
