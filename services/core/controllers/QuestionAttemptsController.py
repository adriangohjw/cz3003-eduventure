from flask import jsonify, request
from flask_restful import Resource

import json

from flask.helpers import make_response

from ..contracts.questionAttempts_contracts import \
    questionAttemptListReadContract, questionAttemptCreateContract

from ..operations.questionAttempts_operations import \
    questionAttemptListReadOperation, questionAttemptCreateOperation

from exceptions import ErrorWithCode

class QuestionAttemptListAPI(Resource):
    def get(self):
        # contracts
        try:
            qa = questionAttemptListReadContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            questionAttemptList = questionAttemptListReadOperation(
                qa['student_id'], qa['question_id']
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
                list = [qa.asdict() for qa in questionAttemptList]
            ), 200
        )

class QuestionAttemptAPI(Resource):
    def post(self):
        # contracts
        try:
            qa = questionAttemptCreateContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            questionAttempt = questionAttemptCreateOperation(
                qa['student_id'], qa['question_id'], qa['is_correct'], qa['duration_ms']
            )
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify(questionAttempt.asdict()), 200
        )
            