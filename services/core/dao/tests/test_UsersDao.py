import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest 

from models import db, User
from run_test import create_app

app = create_app()
app.app_context().push()
db.init_app(app)

from services.core.operations.users_operations import encrypt
from services.core.dao.UsersDAO import userRead, userCreate, userUpdate

class Test_users_dao(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()
        
    def test_userRead(self):

        user = User(
            email = 'john_doe@gmail.com',
            encrypted_password=encrypt('password'),
            name = 'john_doe'
        )

        db.session.add(user)
        db.session.commit()

        user_list = User.query.all()

        self.assertEqual(1, len(user_list))
        self.assertTrue(userRead(col='email', value='john_doe@gmail.com'))
        self.assertTrue(userRead(col='id', value=1))

    
    def test_userCreate(self):
        
        user = User(
            email = 'john_doe@gmail.com',
            encrypted_password=encrypt('password'),
            name = 'john_doe'
        )

        userCreate(user)

        user_list = User.query.all()

        self.assertEqual(1, len(user_list))
        self.assertEqual(user_list[0].email, 'john_doe@gmail.com')

    
    def test_userUpdate(self):

        user = User(
            email = 'john_doe@gmail.com',
            encrypted_password=encrypt('password'),
            name = 'john_doe'
        )

        db.session.add(user)
        db.session.commit()

        password_original = user.encrypted_password
        user.encrypted_password = encrypt('password_new')

        userUpdate()

        user = User.query.filter_by(email='john_doe@gmail.com').first()
        self.assertNotEqual(password_original, user.encrypted_password)

if __name__ == '__main__':
    unittest.main()
