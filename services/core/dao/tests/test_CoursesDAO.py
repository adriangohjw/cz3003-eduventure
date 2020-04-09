import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest

from models import db
from run_test import create_app
app = create_app()
app.app_context().push()
db.init_app(app)

from models import Course
from services.core.dao.CoursesDAO import courseCreate,courseRead


class Test_CoursesDAO(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()


    def test_courseCreate(self):

        self.assertEqual(len(Course.query.all()), 0)

        course = Course(index='cz3003')
        courseCreate(course)

        course_list = Course.query.all()
        self.assertEqual(1, len(course_list))
        self.assertEqual(course_list[0].index, 'cz3003')


    def test_courseRead(self):

        self.assertIsNone(courseRead(index='cz3003'))

        course = Course(index='cz3003')
        db.session.add(course)
        db.session.commit()

        self.assertEqual(courseRead(index='cz3003').index, 'cz3003')


if __name__ == '__main__':
    unittest.main()
