import sys
from os import path, getcwd
sys.path.append(getcwd())

import unittest

from models import db
from run_test import create_app
app = create_app()
app.app_context().push()
db.init_app(app)

from models import Lesson, Topic
from services.core.dao.LessonsDAO import \
    lessonCreate, lessonRead, lessonDelete, lessonUpdate, lessonListRead, getLastLessonID


class Test_LessonsDAO(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()
        
        topic = Topic(name='seng')
        db.session.add(topic)
        db.session.commit()


    def test_lessonCreate(self):

        self.assertEqual(len(Lesson.query.all()), 0)

        lesson = Lesson(topic_id=1, id=3, name='se', content='test')
        lessonCreate(lesson)

        lesson_list = Lesson.query.all()
        self.assertEqual(1, len(lesson_list))
        self.assertEqual(lesson_list[0].topic_id, 1)
        self.assertEqual(lesson_list[0].id, 3)
        self.assertEqual(lesson_list[0].name, 'se')
        self.assertEqual(lesson_list[0].content, 'test')


    def test_lessonRead(self):

        self.assertIsNone(lessonRead(topic_id=1, col='id', value=3))

        lesson = Lesson(topic_id=1, id=3, name='se', content='test')
        db.session.add(lesson)
        db.session.commit()

        self.assertEqual(lessonRead(topic_id=1, col='name', value='se').name, 'se')
        self.assertEqual(lessonRead(topic_id=1, col='id', value=3).name, 'se')
        self.assertFalse(lessonRead(topic_id=1, col='wrong_value', value=3))


    def test_lessonUpdate(self):

        lesson = Lesson(topic_id=1, id=3, name='se', content='test')
        db.session.add(lesson)
        db.session.commit()

        lesson.name = 'softwareEngi'
        lessonUpdate()

        self.assertEqual(
            Lesson.query.filter_by(topic_id=1).filter_by(id=3).first().name,
            'softwareEngi'
        )
        

    def test_lessonDelete(self):

        lesson = Lesson(topic_id=1, id=3, name='se', content='test')
        db.session.add(lesson)
        db.session.commit()

        self.assertEqual(len(Lesson.query.all()), 1)

        lessonDelete(topic_id=1, lesson_id=3)

        self.assertEqual(len(Lesson.query.all()), 0)


    def test_lessonListRead(self):

        self.assertEqual(len(lessonListRead()), 0)
        
        self.assertEqual(
            lessonListRead(),
            []
        )

        lesson = Lesson(topic_id=1, id=1, name='lesson_1', content='content')
        db.session.add(lesson)
        db.session.commit()

        self.assertEqual(len(lessonListRead()), 1)

        self.assertEqual(lessonListRead()[0].name, 'lesson_1')


    def test_getLastLessonID(self):

        self.assertEqual(getLastLessonID(1), 0)

        lesson = Lesson(topic_id=1, id=1, name='se', content='test')
        db.session.add(lesson)
        db.session.commit()

        self.assertEqual(getLastLessonID(1), 1)


if __name__ == '__main__':
    unittest.main()
