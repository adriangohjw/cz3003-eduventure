import sys
from os import path, getcwd

sys.path.append(getcwd())

import unittest

from services.quiz.operations.questionChoices_operations import initializeQuestionChoice,questionChoiceCreateOperation,questionChoiceDeleteOperation,questionChoiceReadOperation,questionChoiceUpdateOperation
from exceptions import ErrorWithCode

from models import db, User, Student,Lesson,Question,Topic, QuestionChoice
from run_test import create_app
from services.core.operations.users_operations import encrypt

app = create_app()
app.app_context().push()
db.init_app(app)


class Test_questionChoices_operations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n\n{}: starting test...".format(path.basename(__file__)))

    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()
        user = User(
            email='john_d@gmail.com',
            encrypted_password=encrypt('password'),
            name='john_doe'
        )
        # db.session.add(user)
        student = Student(user, 'U1722')
        db.session.add(student)
        topic = Topic(name='seng')
        db.session.add(topic)
        lesson = Lesson(topic_id='1', id='3', name='se', content='test')
        db.session.add(lesson)
        qn = Question('1', '3', 'easy')
        db.session.add(qn)
        qa = initializeQuestionChoice(1,'A',False)
        db.session.add(qa)
        db.session.commit()

    def test_questionChoiceCreateOperation(self):
        with self.assertRaises(ErrorWithCode):
            questionChoiceCreateOperation(2,"A",False)

            self.assertIsNotNone(questionChoiceCreateOperation(1,"B",False))

    def test_questionChoiceReadOperation(self):
        with self.assertRaises(ErrorWithCode):
            questionChoiceReadOperation(1,3)

        self.assertIsNotNone( questionChoiceReadOperation(1,1))

    def test_questionChoiceUpdateOperation(self):
        qc = QuestionChoice.query.filter_by(question_id=1).first()
        des_original =qc.description

        questionChoiceUpdateOperation(1,1,'description',None)

        qc = QuestionChoice.query.filter_by(question_id=1).first()
        self.assertNotEqual(des_original, qc.description)

    def test_questionChoiceDeleteOperation(self):
        questionChoiceDeleteOperation(1,1)

        qc = QuestionChoice.query.filter_by(question_id=1).first()
        self.assertIsNone(qc)

if __name__ == '__main__':
    unittest.main()
