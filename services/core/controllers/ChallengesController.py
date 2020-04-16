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
            challenge = challengeCreateOperation(
                c['from_student_id'], c['to_student_id']
            )
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        res = {
            'from_student_id': challenge.from_student_id,
            'to_student_id': challenge.to_student_id,
            'quiz': {
                'id': challenge.quiz_id,
                'questions': []
            },
            'is_completed': challenge.is_completed,
            'winner_id': challenge.winner_id,
            'created_at': challenge.created_at
        }
        for q in challenge.quiz.questions:
            question = q.question
            res['quiz']['questions'].append(
                {
                    'id': question.id,
                    'topic_id': question.topic_id,
                    'lesson_id': question.lesson_id,
                    'description': question.description,
                    'count_choices': len(question.choices),
                    'choices': [z.to_json() for z in question.choices]
                }
            )
        return make_response(
            jsonify(res), 200
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

