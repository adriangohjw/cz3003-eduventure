from flask import jsonify, request, json
from flask_restful import Resource

from models import User
from flask.helpers import make_response

import bcrypt

from ..dao.UsersDAO import userCreate, userRead, userUpdate
from ..contracts.users_contracts import userReadContract
from ..operations.users_operations import userReadOperation
from exceptions import ErrorWithCode

def encrypt(plaintext_password):
    return bcrypt.hashpw(bytes(plaintext_password, "utf8"), bcrypt.gensalt()).decode("utf-8")

def authenticate(plaintext_password, encrypted_password):
    return bcrypt.checkpw(bytes(plaintext_password, "utf-8"), bytes(encrypted_password, "utf-8"))

def initializeUser(email, password):
    email_split = email.split('@')
    name = email_split[0]
    encrypted_password = encrypt(password)
    if (len(email_split) == 2) and (password is not None):
        return User(
            email=email, 
            name=name, 
            encrypted_password=encrypted_password
        )
    else:
        return False

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
            jsonify (user), 200
        )


    def post(self):
        email = request.args.get('email')
        password = request.args.get('password')        
        user = initializeUser(email, password)
        if (userRead(col='email', value=user.email)): # if existing user
            return make_response(
                jsonify (
                    message = "User {} already exist".format(user.email)
                ), 409
            )
        else:
            user_create_status = userCreate(user)
            if (user_create_status):  # if user creation is successful
                return make_response(
                    jsonify(
                        message = "User creation - successful"
                    ), 200
                )
            else:   # if user creation is not successful
                return make_response(
                    jsonify (
                        message = "User creation - precondition failed"
                    ), 412
                )

    def put(self):
        email = request.args.get('email')
        old_password = request.args.get('old_password')
        new_password = request.args.get('new_password')
        user = userRead(col='email', value=email)
        if (user):  # if user can be found
            if (authenticate(old_password, user.encrypted_password)):   # if correct password provided
                user.encrypted_password = encrypt(new_password)
                user_update_status = userUpdate()
                if (user_update_status):    # successful in updating password
                    return make_response(
                        jsonify (
                            message = "Password update successful",
                        ), 200
                    )
                else:   # unsuccessful in updating password
                    return make_response(
                        jsonify (
                            message = "Password update unsuccessful - database error",
                        ), 400
                    )
            else:   # if incorrect password provided
                return make_response(
                    jsonify (
                        message = "Password update unsuccessful - incorrect password provided"
                    ), 401
                )
        else:   # if user cannot be found
            return make_response(
                jsonify (
                    message = "no user found"
                ), 404
            )