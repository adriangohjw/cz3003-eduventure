import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from services.quiz.operations.questions_operations import initializeQuestion,questionCreateOperation,questionDeleteOperation,questionReadOperation,questionUpdateOperation
from exceptions import ErrorWithCode

from models import db, User, Student,Lesson,Question,Topic, QuestionChoice
from run_test import create_app
from services.core.operations.users_operations import encrypt

app = create_app()
app.app_context().push()
db.init_app(app)


class Test_questions_operations(unittest.TestCase):
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
        q = initializeQuestion(1,3,"easy")
        db.session.add(q)
        db.session.commit()

    def test_questionCreateOperation(self):
        with self.assertRaises(ErrorWithCode):
            questionCreateOperation(1,2,"easy")
            questionCreateOperation(2,1, "easy")

            self.assertIsNotNone(questionCreateOperation(1,3, "intermediate"))

    def test_questionReadOperation(self):
        with self.assertRaises(ErrorWithCode):
            questionReadOperation(2)
            questionReadOperation(3)

        self.assertIsNotNone( questionReadOperation(1))

    def test_questionUpdateOperation(self):
        q = Question.query.filter_by(id=1).first()
        des_original =q.description

        questionUpdateOperation(1,"hard")

        q = Question.query.filter_by(id=1).first()
        self.assertNotEqual(des_original, q.description)

    def test_questionDeleteOperation(self):
        questionDeleteOperation(1)

        q = Question.query.filter_by(id=1).first()
        self.assertIsNone(q)

if __name__ == '__main__':
    unittest.main()
