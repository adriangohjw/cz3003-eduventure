from flask import jsonify, request
from flask_restful import Resource

from flask.helpers import make_response

from ..contracts.lessons_contracts import lessonReadContract, lessonCreateContract, lessonUpdateContract, lessonDeleteContract
from ..operations.lessons_operations import lessonReadOperation, lessonCreateOperation, lessonUpdateOperation, lessonDeleteOperation, lessonListReadOperation
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
            lesson = lessonCreateOperation(
                l['topic_id'], l['name'], l['content'], l['url_link']
            )
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


class LessonListAPI(Resource):
    def get(self):
        # operations
        try:
            lessons = lessonListReadOperation()
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify (
                lessons = [lesson.asdict() for lesson in lessons]
            ), 200
        )


from services.core.contracts.rs_lesson_quiz_contains_contracts import \
    quizMngCreateContract, quizMngReadContract, quizMngDeleteContract
from services.core.operations.rs_lesson_quiz_contains_operations import \
    quizMngCreateOperation, quizMngReadOperation, quizMngDeleteOperation

class QuizManagerAPI(Resource):
    def get(self):
        # contracts
        try:
            rs = quizMngReadContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )
        
        # operations
        try:
            relationships = quizMngReadOperation(
                rs['topic_id'], rs['lesson_id']
            )
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify (
                topic_id = rs['topic_id'],
                lesson_id = rs['lesson_id'],
                quiz = [rs.asdict_quizMng() for rs in relationships]
            ), 200
        )
        
    def post(self):
        # contracts
        try:
            rs = quizMngCreateContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            relationship = quizMngCreateOperation(
                rs['topic_id'], rs['lesson_id'], rs['quiz_id']
            )
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify(relationship.asdict()), 200
        )
    
    def delete(self):
        # contracts
        try:
            rs = quizMngDeleteContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            rs = quizMngDeleteOperation(
                rs['id']
            )
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify(
                message = 'Successfully deleted rs'
            ), 200
        )
