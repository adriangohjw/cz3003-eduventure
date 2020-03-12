from flask import Flask, jsonify
from flask_restful import Resource, Api
from config import Hash
from flask_security.utils import hash_password

from models import db, User

class UserAPI(Resource):
    def get(self, email):
        user = User.query.filter_by(email=email).first()
        return jsonify (
            message = "Hello world!",
            email = user.email,
            encrypted_password = user.encrypted_password,
            name = user.name
        )

    def post(self, email, password, name):
        encrypted_password = hash_password(password)
        print(">>> email:{}, password:{}".format(email, encrypted_password))
        user = User(email=email, name=name, encrypted_password=encrypted_password)
        db.session.add(user)
        db.session.commit()