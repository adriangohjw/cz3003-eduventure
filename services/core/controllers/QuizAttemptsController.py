from flask import jsonify, request
from flask_restful import Resource

from flask.helpers import make_response

from ..contracts.quizAttempts_contracts import \
    quizAttemptListReadContract, quizAttemptCreateContract

from ..operations.quizAttempts_operations import \
    quizAttemptListReadOperation, quizAttemptCreateOperation

from exceptions import ErrorWithCode

class QuizAttemptListAPI(Resource):
    def get(self):
        # contracts
        try:
            qas = quizAttemptListReadContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            quizAttemptList = quizAttemptListReadOperation(
                qas['student_id'], qas['quiz_id']
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
                list = [qa.asdict() for qa in quizAttemptList]
            ), 200
        )

class QuizAttemptAPI(Resource):
    def post(self):
        # contracts
        try:
            qa = quizAttemptCreateContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            quizAttempt = quizAttemptCreateOperation(
                qa['student_id'], qa['quiz_id'], qa['score']
            )
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify(quizAttempt.asdict()), 200
        )
                