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
from services.core.dao.CoursesDAO import (
    courseCreate,
    courseRead
)


"""
This is a TestCase object to test the functions in CoursesDAO.py
"""
class Test_CoursesDAO(unittest.TestCase):
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

    # test the function courseCreate
    def test_courseCreate(self):

        # create a new Course object
        course = Course(index='cz3003')
        
        # add Course object to the database
        courseCreate(course)

        # retrieve all records from the table 'courses'
        course_list = Course.query.all()

        # check that the number of record added is correct
        print('--- check that the number of record added is correct')
        self.assertEqual(1, len(course_list))

        # check that the value(s) of the Course object added is correct
        print('--- check that the value(s) of the Course object added is correct')
        self.assertEqual(course_list[0].index, 'cz3003')

    # test the function courseRead
    def test_courseRead(self):

        # create a new Course object and add it to the database
        course = Course(index='cz3003')
        db.session.add(course)
        db.session.commit()

        # check that the record retrieved is correct
        print('--- check that the record retrieved is correct')
        self.assertEqual(courseRead(index='cz3003').index, 'cz3003')


if __name__ == '__main__':
    unittest.main(verbosity=2)
