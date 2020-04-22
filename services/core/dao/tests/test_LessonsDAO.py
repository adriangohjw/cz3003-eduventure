import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest

from models import db
from run_test import create_app
app = create_app()
app.app_context().push()
db.init_app(app)

from models import (
    Lesson, Topic
)
from services.core.dao.LessonsDAO import (
    lessonCreate, 
    lessonRead, 
    lessonDelete, 
    lessonUpdate, 
    lessonListRead, 
    getLastLessonID
)
    

"""
This is a TestCase object to test the functions in LessonsDAO.py
"""
class Test_LessonsDAO(unittest.TestCase):
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
        
        # adding topics
        topic = Topic(name='seng')
        db.session.add(topic)
        db.session.commit()

    # test the function lessonCreate
    def test_lessonCreate(self):

        # create a new Lesson object
        lesson = Lesson(topic_id=1, id=3, name='se', content='test')

        # add Lesson object to the database
        lessonCreate(lesson)

        # retrieve all records from the table 'lessons'
        lesson_list = Lesson.query.all()

        # check that the number of record added is correct
        print('--- check that the number of record added is correct')
        self.assertEqual(1, len(lesson_list))

        # check that the value(s) of the Lesson object added is correct
        print('--- check that the value(s) of the Lesson object added is correct')
        self.assertEqual(lesson_list[0].topic_id, 1)
        self.assertEqual(lesson_list[0].id, 3)
        self.assertEqual(lesson_list[0].name, 'se')
        self.assertEqual(lesson_list[0].content, 'test')

    # test the function lessonRead
    def test_lessonRead(self):

        # create a new Lesson object and add it to the database
        lesson = Lesson(topic_id=1, id=3, name='se', content='test')
        db.session.add(lesson)
        db.session.commit()

        # check that the record retrieved is correct (using col='name')
        print('--- check that the record retrieved is correct (using col=\'name\')')
        self.assertEqual(lessonRead(topic_id=1, col='name', value='se').name, 'se')

        # check that the record retrieved is correct (using col='id')
        print('--- check that the record retrieved is correct (using col=\'id\')')
        self.assertEqual(lessonRead(topic_id=1, col='id', value=3).name, 'se')

        # check that no record is retrieved (when value of col is unacceptable
        print('--- check that no record is retrieved (when value of col is unacceptable')
        self.assertFalse(lessonRead(topic_id=1, col='wrong_value', value=3))

    # test the function lessonUpdate
    def test_lessonUpdate(self):

        # create a new Lesson object and add it to the database
        lesson = Lesson(topic_id=1, id=3, name='se', content='test')
        db.session.add(lesson)
        db.session.commit()

        # update value of Lesson object
        lesson.name = 'softwareEngi'
        lessonUpdate()

        # fetch updated Lesson object from the database
        lesson = Lesson.query.filter_by(topic_id=1).filter_by(id=3).first()

        # check if value of Lesson object has been updated
        print('--- check if value of Lesson object has been updated')
        self.assertEqual(lesson.name, 'softwareEngi')
        
    # test the function lessonDelete
    def test_lessonDelete(self):

        # create a new Lesson object and add it to the database
        lesson = Lesson(topic_id=1, id=3, name='se', content='test')
        db.session.add(lesson)
        db.session.commit()

        # check that record has been deleted (number of record in database -1)
        print('--- check that record has been deleted (-1 number of record in database)')
        self.assertEqual(len(Lesson.query.all()), 1)
        lessonDelete(topic_id=1, lesson_id=3)
        self.assertEqual(len(Lesson.query.all()), 0)

    # test the function lessonListRead
    def test_lessonListRead(self):
        
        # check that function returns the right result (when number of record = 0)
        print('--- check that function returns the right result (when number of record = 0)')
        self.assertEqual(len(lessonListRead()), 0)
        self.assertEqual(
            lessonListRead(), []
        )

        # create a new Lesson object and add it to the database
        lesson = Lesson(topic_id=1, id=1, name='lesson_1', content='content')
        db.session.add(lesson)
        db.session.commit()

        # check that function returns the right result (when number of record = 1)
        print('--- check that function returns the right result (when number of record = 1)')
        self.assertEqual(len(lessonListRead()), 1)
        self.assertEqual(lessonListRead()[0].name, 'lesson_1')

    # test the function getLastLessonID
    def test_getLastLessonID(self):

        # check that function returns 0 when no record in the table
        print('--- check that function returns 0 when no record in the table')
        self.assertEqual(getLastLessonID(1), 0)

        # create a new Lesson object and add it to the database
        lesson = Lesson(topic_id=1, id=1, name='se', content='test')
        db.session.add(lesson)
        db.session.commit()

        # check that function returns 1 when no record in the table
        print('--- check that function returns 1 when no record in the table')
        self.assertEqual(getLastLessonID(1), 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
