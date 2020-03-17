from flask import Blueprint
from flask_restful import Api

from services.quiz.controllers import \
    QuestionsController, QuestionChoicesController

question_bp = Blueprint('question', __name__)
api_question = Api(question_bp)
api_question.add_resource(QuestionsController.QuestionAPI, '/')

questionchoice_bp = Blueprint('questionchoice', __name__)
api_questionchoice = Api(questionchoice_bp)
api_questionchoice.add_resource(QuestionChoicesController.QuestionChoiceAPI, '/')