from flask import jsonify, request
from flask_restful import Resource

from flask.helpers import make_response

from exceptions import ErrorWithCode

from services.core.contracts.progresses_contracts import progressReadContract
from services.core.operations.progresses_operations import progressReadOperation


class ProgressAPI(Resource):
    def get(self):
        # contracts
        try:
            p = progressReadContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            progresses = progressReadOperation(
                p['student_id']
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
                progresses
            ), 200
        )
