from flask import jsonify, request
from flask_restful import Resource, Api

from models import db, User, Staff
from flask.helpers import make_response

import requests
import bcrypt

from .UsersController import is_existing, create_user

class StaffAPI(Resource):
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
