from flask import Blueprint
from flask_restful import Api

from services.quiz.resources import \
    QuestionsController

question_bp = Blueprint('question', __name__)
api_question = Api(question_bp)
api_question.add_resource(QuestionsController.QuestionAPI, '/')