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

from services.core.dao.StudentsDAO import studentCreate,studentRead,studentUpdate


class Test_StudentsDAO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()

    def test_studentCreate(self):
        user = User(
            email='student@gmail.com',
            encrypted_password=encrypt('password'),
            name='std'
        )
        std = Student(user=user,matriculation_number="U1722")

        studentCreate(std)

        std_list = Student.query.all()

        self.assertEqual(1, len(std_list))
        self.assertEqual(std_list[0].email,'student@gmail.com')

    def test_studentRead(self):
        user = User(
            email='student@gmail.com',
            encrypted_password=encrypt('password'),
            name='std'
        )
        std = Student(user=user, matriculation_number="U1722")

        db.session.add(std)
        db.session.commit()

        std_list = Student.query.all()

        self.assertTrue(studentRead('email','student@gmail.com'))
        self.assertTrue(studentRead('id',1))

    def test_studentUpdate(self):
        user = User(
            email='student@gmail.com',
            encrypted_password=encrypt('password'),
            name='std'
        )
        std = Student(user=user, matriculation_number="U1722")

        db.session.add(std)
        db.session.commit()

        name_original =std.name
        std.name = 'Justin'

        studentUpdate()

        std = Student.query.filter_by(email='student@gmail.com').first()
        self.assertNotEqual(name_original, std.name)


if __name__ == '__main__':
    unittest.main()
