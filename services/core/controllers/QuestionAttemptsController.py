from flask import jsonify, request
from flask_restful import Resource

import json

from flask.helpers import make_response

from ..contracts.questionAttempts_contracts import \
    questionAttemptListReadContract, questionAttemptCreateContract

from ..operations.questionAttempts_operations import \
    questionAttemptListReadOperation, questionAttemptCreateOperation, questionAttemptLeaderboardOperation

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
            

class QuestionAttemptLeaderboardAPI(Resource):

    def get(self):

        # operations
        try:
            questionAttemptLeaderboard = questionAttemptLeaderboardOperation()
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        record_list = []
        for record_result in questionAttemptLeaderboard:
            record = record_result._asdict()
            record_list.append(
                {
                'id': record['student_id'],
                'name': record['student_name'],
                'email': record['student_email'],
                'score': record['total_score']
                }
            )
                    
        return make_response(
            jsonify (
                students = record_list
            ), 200
        )
        