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

from services.core.dao.StaffsDAO import staffCreate,staffRead,staffUpdate


class Test_StaffsDAO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()

    def test_staffCreate(self):
        user = User(
            email='staff@gmail.com',
            encrypted_password=encrypt('password'),
            name='staff'
        )
        stf = Staff(user=user)

        staffCreate(stf)

        stf_list = Staff.query.all()

        self.assertEqual(1, len(stf_list))
        self.assertEqual(stf_list[0].email,'staff@gmail.com')

    def test_staffRead(self):
        user = User(
            email='staff@gmail.com',
            encrypted_password=encrypt('password'),
            name='staff'
        )
        stf = Staff(user=user)

        db.session.add(stf)
        db.session.commit()

        stf_list = Staff.query.all()

        self.assertTrue(staffRead('email','staff@gmail.com'))
        self.assertTrue(staffRead('id',1))

    def test_staffUpdate(self):
        user = User(
            email='staff@gmail.com',
            encrypted_password=encrypt('password'),
            name='staff'
        )
        stf = Staff(user=user)

        db.session.add(stf)
        db.session.commit()

        name_original =stf.name
        stf.name = 'Justin'

        staffUpdate()

        stf = Staff.query.filter_by(email='staff@gmail.com').first()
        self.assertNotEqual(name_original, stf.name)


if __name__ == '__main__':
    unittest.main()
