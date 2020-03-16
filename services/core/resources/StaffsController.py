from flask import jsonify, request
from flask_restful import Resource

from models import db, User, Staff, Course
from flask.helpers import make_response

import requests

from .UsersController import is_existing, create_user

def is_staff(col, value):
    if (col == 'email'):
        user = User.query.filter_by(email=email).first()
        return bool(Staff.query.filter_by(id=user.id).first())
    if (col == 'id'):
        return bool(Staff.query.filter_by(id=id).first())

def getStaff(col, value):
    if (is_staff(col=col, value=value)):
        if (col == 'name'):
            return Staff.query.filter_by(name=value).first()
        elif (col == 'id'):
            return Staff.query.filter_by(id=value).first()
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