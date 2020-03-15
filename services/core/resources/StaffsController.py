from flask import jsonify, request
from flask_restful import Resource, Api

from models import db, User, Staff
from flask.helpers import make_response

import requests
import bcrypt

from .UsersController import is_existing, create_user

def is_staff(email):
    user = User.query.filter_by(email=email).first()
    if (user is not None):
        return bool(Staff.query.filter_by(id=user.id).first())
    else:
        return False

class StaffAPI(Resource):
    def get(self):
        email = request.args.get('email')
        if (is_staff(email)):
            return make_response(
                jsonify(
                    message = "User is staff"
                ), 200
            )
        else:
            return make_response(
                jsonify(
                    message = "User is not staff / does not exist"
                ), 404
            )

    def post(self):
        email = request.args.get('email')
        if (is_existing(email)):
            return make_response(
                jsonify(
                    message = "Staff already exist"
                ), 400
            )
        password = request.args.get('password')
        user = create_user(email, password)
        if (user):
            staff = Staff(user)
            db.session.add(staff)
            db.session.commit()
            return make_response(
                jsonify(
                    message = "Staff creation - successful"
                ), 200
            )
        else:  
            return make_response(
                jsonify (
                    message = "Staff creation - precondition failed"
                ), 412
            )
