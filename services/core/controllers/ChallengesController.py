from flask import jsonify, request
from flask_restful import Resource

from flask.helpers import make_response

from exceptions import ErrorWithCode

from services.core.contracts.challenges_contracts import \
    challengeCreateContract, challengeReadContract, challengeUpdateCompletedContract

from services.core.operations.challenges_operations import \
    challengeCreateOperation, challengeReadOperation, challengeUpdateCompletedOperation


class ChallengeAPI(Resource):

    def get(self):
        # contracts
        try:
            c = challengeReadContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            challenges = challengeReadOperation(
                c['from_student_id'], c['to_student_id'], c['quiz_id'], c['is_completed']
            )
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify ([c.asdict() for c in challenges]), 200
        )


    def post(self):
        # contracts
        try:
            c = challengeCreateContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            lesson = challengeCreateOperation(
                c['from_student_id'], c['to_student_id'], c['quiz_id']
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
            c = challengeUpdateCompletedContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )    
        
        # operations
        try:
            challenge = challengeUpdateCompletedOperation(
                c['from_student_id'], c['to_student_id'], c['quiz_id'], c['winner_id']
            )
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify(challenge.asdict()), 200
        )

