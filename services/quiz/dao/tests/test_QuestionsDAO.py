import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from models import db, Question,Topic,Lesson
from run_test import create_app

app = create_app()
app.app_context().push()
db.init_app(app)

from services.quiz.dao.QuestionsDAO import \
    questionCreate, questionDelete, questionRead, questionUpdate, \
    questionGetAllRead


class Test_QuestionsDAO(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))


    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()
        topic = Topic(name='seng')
        db.session.add(topic)
        lesson = Lesson(topic_id='1', id='3', name='se', content='test')
        db.session.add(lesson)
        db.session.commit()


    def test_questionCreate(self):

        qn = Question('1', '3', 'easy')
        questionCreate(qn)

        qn_list = Question.query.all()

        self.assertEqual(1, len(qn_list))
        self.assertEqual(qn_list[0].topic_id, 1)


    def test_questionRead(self):

        qn = Question('1', '3', 'easy')

        db.session.add(qn)
        db.session.commit()

        self.assertTrue(questionRead(1))


    def test_questionUpdate(self):

        qn = Question('1', '3', 'easy')

        db.session.add(qn)
        db.session.commit()

        des_original = qn.description
        qn.description = "Intermediate"

        questionUpdate

        qn =Question.query.filter_by(topic_id=1).first()
        self.assertNotEqual(des_original, qn.description)


    def test_questionDelete(self):

        qn = Question('1', '3', 'easy')

        db.session.add(qn)
        db.session.commit()

        self.assertEqual(1, len(Question.query.all()))

        questionDelete(1)

        self.assertEqual(0, len(Question.query.all()))


    def test_questionGetAllRead(self):

        self.assertEqual(len(questionGetAllRead()), 0)

        qn1 = Question('1', '3', 'question_1')
        db.session.add(qn1)
        qn2 = Question('1', '3', 'question_2')
        db.session.add(qn2)
        qn3 = Question('1', '3', 'question_3')
        db.session.add(qn3)
        db.session.commit()

        self.assertEqual(len(questionGetAllRead()), 3)


if __name__ == '__main__':
    unittest.main()
