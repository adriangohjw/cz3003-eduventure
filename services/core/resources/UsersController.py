from flask import jsonify, request
from flask_restful import Resource, Api

from models import db, User
from flask.helpers import make_response
from config import POSTGRES_URL

import requests
import bcrypt

def encrypt(plaintext_password):
    return bcrypt.hashpw(bytes(plaintext_password, "utf8"), bcrypt.gensalt()).decode("utf-8")

def authenticate(plaintext_password, encrypted_password):
    return bcrypt.checkpw(bytes(plaintext_password, "utf-8"), bytes(encrypted_password, "utf-8"))

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
        if (bool(User.query.filter_by(email=email).first())):
            return make_response(
                jsonify(
                    message = "User already exist"
                ), 400
            )
        password = request.args.get('password')
        email_split = email.split('@')
        if (len(email_split) == 2) and (password is not None):
            name = email_split[0]
            encrypted_password = encrypt(password)
            user = User(
                email=email, 
                name=name, 
                encrypted_password=encrypted_password
            )
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