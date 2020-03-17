from flask import jsonify, request
from flask_restful import Resource

from flask.helpers import make_response

from ..contracts.users_contracts import userReadContract, userCreateContract, userUpdateContract
from ..operations.users_operations import initializeUser, userReadOperation, userCreateOperation, userUpdateOperation
from exceptions import ErrorWithCode

class UserAPI(Resource):
    def get(self):
        # contracts
        try:
            u = userReadContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            user = userReadOperation(u['email'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify (user.asdict()), 200
        )


    def post(self):
        # contracts
        try:
            u = userCreateContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            user = userCreateOperation(u['email'], u['password'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify(user.asdict()), 200
        )
        

    def put(self):
        # contracts
        try:
            u = userUpdateContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            user = userUpdateOperation(u['email'], u['old_password'], u['new_password'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify(user.asdict()), 200
        )
            