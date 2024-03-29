from flask import Blueprint
from flask_restful import Api

from services.quiz.controllers import \
    QuizzesController, QuestionsController, QuestionChoicesController

quiz_bp = Blueprint('quiz', __name__)
api_quiz = Api(quiz_bp)
api_quiz.add_resource(QuizzesController.QuizAPI, '/')
api_quiz.add_resource(QuizzesController.CourseManagerAPI, '/courses')
api_quiz.add_resource(QuizzesController.QuestionManagerAPI, '/questions')
api_quiz.add_resource(QuizzesController.QuizOverallAPI, '/overall')

question_bp = Blueprint('question', __name__)
api_question = Api(question_bp)
api_question.add_resource(QuestionsController.QuestionAPI, '/')
api_question.add_resource(QuestionsController.QuestionGetAllAPI, '/all/')

questionchoice_bp = Blueprint('questionchoice', __name__)
api_questionchoice = Api(questionchoice_bp)
api_questionchoice.add_resource(QuestionChoicesController.QuestionChoiceAPI, '/')