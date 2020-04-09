from flask import jsonify, request
from flask_restful import Resource

from flask.helpers import make_response

from ..contracts.questions_contracts import questionReadContract, questionCreateContract, questionUpdateContract, questionDeleteContract
from ..operations.questions_operations import questionReadOperation, questionCreateOperation, questionUpdateOperation, questionDeleteOperation
from exceptions import ErrorWithCode

class QuestionAPI(Resource):
    def get(self):
        # contracts
        try:
            q = questionReadContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            question = questionReadOperation(q['id'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify (question.asdict()), 200
        )

    def post(self):
        # contracts
        try:
            q = questionCreateContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            question = questionCreateOperation(q['topic_id'], q['lesson_id'], q['description'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify(question.asdict()), 200
        )

    def put(self):
        # contracts
        try:
            q = questionUpdateContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )    
        
        # operations
        try:
            question = questionUpdateOperation(q['id'], q['description'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify(question.asdict()), 200
        )

    def delete(self):
        # contracts
        try:
            q = questionDeleteContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )    
        
        # operations
        try:
            question = questionDeleteOperation(q['id'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify(
                message = 'Successfully deleted question'
            ), 200
        )


from ..operations.questions_operations import questionGetAllReadOperation

class QuestionGetAllAPI(Resource):
    def get(self):
        # operations
        try:
            questions = questionGetAllReadOperation()
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify (
                questions = [q.asdict() for q in questions]
            ), 200
        )
