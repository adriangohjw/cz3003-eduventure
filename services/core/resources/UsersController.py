from flask import jsonify, request
from flask_restful import Resource

from models import db, User
from flask.helpers import make_response

import requests
import bcrypt

def encrypt(plaintext_password):
    return bcrypt.hashpw(bytes(plaintext_password, "utf8"), bcrypt.gensalt()).decode("utf-8")

def authenticate(plaintext_password, encrypted_password):
    return bcrypt.checkpw(bytes(plaintext_password, "utf-8"), bytes(encrypted_password, "utf-8"))

def is_existing(email):
    return bool(User.query.filter_by(email=email).first())

def create_user(email, password):
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
        False

class UserAPI(Resource):
    def get(self):
        email = request.args.get('email')
        user = User.query.filter_by(email=email).first()
        if user is not None:        
            return make_response(
                jsonify (
                    message = "Hello world!",
                    email = user.email,
                    encrypted_password = user.encrypted_password,
                    name = user.name
                ), 200
            )
        else: 
            return make_response(
                jsonify (
                    message = "no user found"
                ), 404
            )

    def post(self):
        email = request.args.get('email')
        if (is_existing(email)):
            return make_response(
                jsonify(
                    message = "User already exist"
                ), 400
            )
        password = request.args.get('password')
        user = create_user(email, password)
        if (user):
            db.session.add(user)
            db.session.commit()
            return make_response(
                jsonify(
                    message = "User creation - successful"
                ), 200
            )
        else:  
            return make_response(
                jsonify (
                    message = "User creation - precondition failed"
                ), 412
            )

class UserResetPasswordAPI(Resource):
    def put(self):
        email = request.args.get('email')
        old_password = request.args.get('old_password')
        new_password = request.args.get('new_password')
        user = User.query.filter_by(email=email).first()
        if user is not None:  
            if (authenticate(old_password, user.encrypted_password)):
                user.encrypted_password = encrypt(new_password)
                db.session.commit()
                return make_response(
                    jsonify (
                        message = "Password update - successful",
                    ), 200
                )
            else:
                return make_response(
                    jsonify (
                        message = "Password update - unsuccessful"
                    ), 401
                )
        else: 
            return make_response(
                jsonify (
                    message = "no user found"
                ), 404
            )