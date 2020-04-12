from flask import jsonify, request
from flask_restful import Resource

from flask.helpers import make_response

from ..contracts.questionChoices_contracts import \
    questionChoiceReadContract, questionChoiceCreateContract, \
    questionChoiceUpdateContract, questionChoiceDeleteContract

from ..operations.questionChoices_operations import \
    questionChoiceReadOperation, questionChoiceCreateOperation, \
    questionChoiceUpdateOperation, questionChoiceDeleteOperation
from exceptions import ErrorWithCode

class QuestionChoiceAPI(Resource):
    def get(self):
        # contracts
        try:
            qc = questionChoiceReadContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            questionChoice = questionChoiceReadOperation(qc['question_id'], qc['questionChoice_id'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify (questionChoice.asdict()), 200
        )

    def post(self):
        # contracts
        try:
            qc = questionChoiceCreateContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            questionChoice = questionChoiceCreateOperation(qc['question_id'], qc['description'], qc['is_correct'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify(questionChoice.asdict()), 200
        )

    def put(self):
        # contracts
        try:
            qc = questionChoiceUpdateContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )    
        
        # operations
        try:
            questionChoice = questionChoiceUpdateOperation(
                qc['question_id'], qc['questionChoice_id'], qc['description'], qc['is_correct']
            )
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify(questionChoice.asdict()), 200
        )

    def delete(self):
        # contracts
        try:
            qc = questionChoiceDeleteContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )    
        
        # operations
        try:
            questionChoice = questionChoiceDeleteOperation(qc['question_id'], qc['questionChoice_id'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify(
                message = 'Successfully deleted question choice'
            ), 200
        )