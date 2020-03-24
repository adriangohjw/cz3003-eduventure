import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from models import db, Lesson,Topic
from run_test import create_app

app = create_app()
app.app_context().push()
db.init_app(app)

from services.core.dao.LessonsDAO import lessonCreate,lessonRead,lessonDelete,lessonUpdate,getLastLessonID


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
        lesson = Lesson(topic_id='1', id='3', name='se', content='test'
        )

        lessonCreate(lesson)

        lesson_list = Lesson.query.all()

        self.assertEqual(1, len(lesson_list))
        self.assertEqual(lesson_list[0].id,3)
        self.assertEqual(lesson_list[0].name, 'se')
        self.assertEqual(lesson_list[0].content, 'test')


    def test_lessonRead(self):
        lesson = Lesson(topic_id='1', id='3', name='se', content='test'
                        )

        db.session.add(lesson)
        db.session.commit()

        lesson_list = Lesson.query.all()

        self.assertEqual(1, len(lesson_list))
        self.assertTrue(lessonRead(topic_id='1', col='id', value='3'))

    def test_lessonUpdate(self):
        lesson = Lesson(topic_id='1', id='3', name='se', content='test'
                        )

        db.session.add(lesson)
        db.session.commit()

        name_original =lesson.name
        lesson.name = 'softwareEngi'

        lessonUpdate()

        lesson = Lesson.query.filter_by(topic_id='1').filter_by(id='3').first()
        self.assertNotEqual(name_original, lesson.name)

    def test_lessonDelete(self):
        lesson = Lesson(topic_id='1', id='3', name='se', content='test'
                        )

        db.session.add(lesson)
        db.session.commit()

        lessonDelete(topic_id='1',lesson_id='3')

        lesson = Lesson.query.filter_by(topic_id='1').filter_by(id='3').first()
        self.assertIsNone(lesson)

    def test_getLastLessonID(self):
        l = Lesson(1,2,"lesson2","srs")
        db.session.add(l)
        db.session.commit()

        l = Lesson(1, 3, "lesson3", "patterns")
        db.session.add(l)
        db.session.commit()
        lastl = getLastLessonID(1)

        self.assertEqual(lastl, 2)

if __name__ == '__main__':
    unittest.main()
