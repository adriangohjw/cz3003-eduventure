from flask import jsonify, request
from flask_restful import Resource, Api

from models import db, User, Student
from flask.helpers import make_response

import requests
import bcrypt

from .UsersController import is_existing, create_user

def is_student(email):
    user = User.query.filter_by(email=email).first()
    if (user is not None):
        return bool(Student.query.filter_by(id=user.id).first())
    else:
        return False

class StudentAPI(Resource):
    def get(self):
        email = request.args.get('email')
        if (is_student(email)):
            return make_response(
                jsonify(
                    message = "User is Student"
                ), 200
            )
        else:
            return make_response(
                jsonify(
                    message = "User is not student / does not exist"
                ), 404
            )

    def post(self):
        email = request.args.get('email')
        if (is_existing(email)):
            return make_response(
                jsonify(
                    message = "Student already exist"
                ), 400
            )
        password = request.args.get('password')
        matriculation_number = request.args.get('matriculation_number')
        user = create_user(email, password)
        if (user):
            student = Student(user, matriculation_number=matriculation_number)
            db.session.add(student)
            db.session.commit()
            return make_response(
                jsonify(
                    message = "Student creation - successful"
                ), 200
            )
        else:  
            return make_response(
                jsonify (
                    message = "Student creation - precondition failed"
                ), 412
            )
