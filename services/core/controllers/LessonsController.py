from flask import jsonify, request
from flask_restful import Resource

from flask.helpers import make_response

from ..contracts.lessons_contracts import lessonReadContract, lessonCreateContract, lessonUpdateContract, lessonDeleteContract
from ..operations.lessons_operations import lessonReadOperation, lessonCreateOperation, lessonUpdateOperation, lessonDeleteOperation
from exceptions import ErrorWithCode

class LessonAPI(Resource):
    def get(self):
        # contracts
        try:
            l = lessonReadContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            lesson = lessonReadOperation(l['topic_id'], l['lesson_id'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify (lesson.asdict()), 200
        )

    def post(self):
        # contracts
        try:
            l = lessonCreateContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            lesson = lessonCreateOperation(l['topic_id'], l['name'], l['content'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify(lesson.asdict()), 200
        )

    def put(self):
        # contracts
        try:
            l = lessonUpdateContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )    
        
        # operations
        try:
            lesson = lessonUpdateOperation(l['topic_id'], l['lesson_id'], l['col'], l['value'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify(lesson.asdict()), 200
        )
    
    def delete(self):
        # contracts
        try:
            l = lessonDeleteContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )    
        
        # operations
        try:
            lesson = lessonDeleteOperation(l['topic_id'], l['lesson_id'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify(
                message = 'Successfully deleted lesson'
            ), 200
        )
