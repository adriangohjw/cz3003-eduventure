import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from models import db, Question,Topic,Lesson,QuestionChoice
from run_test import create_app
from datetime import datetime

app = create_app()
app.app_context().push()
db.init_app(app)

from services.quiz.dao.QuestionChoicesDAO import questionChoiceCreate,questionChoiceDelete,questionChoiceRead,questionChoiceUpdate,getLastQuestionChoiceID



class Test_QuestionChoicesDAO(unittest.TestCase):
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
        qn = Question('1', '3', 'easy')
        db.session.add(qn)
        db.session.commit()

    def test_questionChoiceCreate(self):
        qnCh = QuestionChoice(1,1,"A",False)
        questionChoiceCreate(qnCh)

        qnCh_list = QuestionChoice.query.all()

        self.assertEqual(1, len(qnCh_list))
        self.assertEqual(qnCh_list[0].question_id, 1)

    def test_questionChoiceRead(self):
        qnCh = QuestionChoice(1, 1, "A", False)

        db.session.add(qnCh)
        db.session.commit()
        self.assertTrue(questionChoiceRead(1,1))

    def test_questionChoiceUpdate(self):
        qnCh = QuestionChoice(1, 1, "A", False)

        db.session.add(qnCh)
        db.session.commit()

        ans_original = qnCh.is_correct
        qnCh.is_correct=True

        questionChoiceUpdate

        qnCh =QuestionChoice.query.filter_by(question_id=1).filter_by(id=1).first()
        self.assertNotEqual(ans_original, qnCh.is_correct)

    def test_questionChoiceDelete(self):
        qnCh = QuestionChoice(1, 1, "A", False)

        db.session.add(qnCh)
        db.session.commit()

        self.assertEqual(1, len(QuestionChoice.query.all()))

        questionChoiceDelete(1,1)

        self.assertEqual(0, len(QuestionChoice.query.all()))

    #not working when the first choice id is larger than the second, meaning they are not ordered by datetime
    def test_getLastQuestionChoiceID(self):
        qnCh = QuestionChoice(1, 4, "B", False)
        db.session.add(qnCh)
        db.session.commit()
        #need to commit separately
        qnChLast = QuestionChoice(1, 2, "C", True)
        db.session.add(qnChLast)

        db.session.commit()
        lastQnCh = getLastQuestionChoiceID(1)

        self.assertEqual(lastQnCh, 2)

if __name__ == '__main__':
    unittest.main()
