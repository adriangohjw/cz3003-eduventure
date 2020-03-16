from flask import jsonify, request
from flask_restful import Resource

from models import db, Question
from flask.helpers import make_response

from ..dao.QuestionsDAO import questionCreate, questionRead, questionUpdate
from ...core.dao.LessonsDAO import lessonRead

def initializeQuestion(topic_id, lesson_id, description):
    lesson = lessonRead(topic_id=topic_id, col='id', value=lesson_id)
    if (lesson and (description is not None)):
        return Question(topic_id, lesson_id, description)
    else:
        return False

class QuestionAPI(Resource):
    def get(self):
        question_id = request.args.get('id')
        question = questionRead(id=question_id)
        if (question):  # question can be found
            return make_response(
                jsonify (
                    id = question.id,
                    topic_id = question.topic_id,
                    lesson_id = question.lesson_id,
                    description = question.description,
                    created_at = question.created_at,
                    count_choices = len(question.choices),
                    choices = question.choices,
                    count_attempts = len(question.attempts),
                    attempts = question.attempts
                ), 200
            )
        else:   # if question cannot be found
            return make_response(
                jsonify (
                    message = "no question found"
                ), 404
            )

    def post(self):
        topic_id = request.args.get('topic_id')
        lesson_id = request.args.get('lesson_id')
        description = request.args.get('description')
        question = initializeQuestion(topic_id=topic_id, lesson_id=lesson_id, description=description)
        lesson = lessonRead(topic_id=topic_id, col='id', value=lesson_id)
        if (lesson):    # topic and lesson exist
            question_create_status = questionCreate(question)
            if (question_create_status):    # if question creation is successful
                return make_response(
                    jsonify(
                        message = "Question creation - successful"
                    ), 200
                )
            else:   # if question creation is not successful
                return make_response(
                    jsonify (
                        message = "Question creation - precondition failed"
                    ), 412
                )
        else:   # topic and/or lesson does not exist
            return make_response(
                jsonify (
                    message = "Question creation - topic/lesson does not exist"
                ), 412
            )
    
    def put(self):
        question_id = request.args.get('id')
        description = request.args.get('description')
        question = questionRead(id=question_id)
        if (question):    # question exist
            question.description = description
            question_update_status = questionUpdate()
            if (question_update_status):    # if question update is successful
                return make_response(
                    jsonify(
                        message = "Question creation - successful"
                    ), 200
                )
            else:   # if question update is not successful
                return make_response(
                    jsonify (
                        message = "Question update unsuccessful - precondition failed"
                    ), 412
                )
        else:   # question does not exist
            return make_response(
                jsonify (
                    message = "Question update unsuccessful - topic/lesson does not exist"
                ), 412
            )