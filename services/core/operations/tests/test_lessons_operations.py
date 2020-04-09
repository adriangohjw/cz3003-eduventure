import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from services.core.operations.lessons_operations import initializeLesson,lessonCreateOperation,lessonReadOperation,lessonDeleteOperation,lessonUpdateOperation

from exceptions import ErrorWithCode

from models import db, Topic,Lesson
from run_test import create_app

app = create_app()
app.app_context().push()
db.init_app(app)


class Test_lessons_operations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()
        topic = Topic(name='seng')
        db.session.add(topic)
        l = initializeLesson(1,'lesson1','srs', 'https://www.google.com')
        db.session.add(l)
        db.session.commit()


    def test_lessonReadOperation(self):
        with self.assertRaises(ErrorWithCode):
            lessonReadOperation(1,2)

        self.assertIsNotNone(lessonReadOperation(1,1))

    def test_lessonCreateOperation(self):
        with self.assertRaises(ErrorWithCode):
            lessonCreateOperation(1,'lesson1','srs','https://www.google.com')

        self.assertTrue(lessonCreateOperation(1,"lesson2","patterns",'https://www.google.com'))

    def test_lessonUpdateOperation(self):
        with self.assertRaises(ErrorWithCode):
            lessonUpdateOperation(1,2,"name","patterns")

        self.assertTrue(lessonUpdateOperation(1,1,"name","lesson3"))

    def test_lessonDeleteOperation(self):
        lessonDeleteOperation(1,1)
        lesson = Lesson.query.filter_by(topic_id=1).filter_by(id=1).first()
        self.assertIsNone(lesson)

if __name__ == '__main__':
    unittest.main()
