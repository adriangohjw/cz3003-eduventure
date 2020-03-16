from flask import jsonify, request
from flask_restful import Resource

from models import db, Course, Staff
from flask.helpers import make_response

import requests

from .StaffsController import is_staff

def create_course(index):
    if (index is not None):
        return Course(index)
    else:
        return False

def is_course(index):
    return bool(Course.query.filter_by(index=index).first())

class CourseAPI(Resource):
    def get(self):
        index = request.args.get('index')
        if (is_course(index)):        
            return make_response(
                jsonify (
                    message = "Course found"
                ), 200
            )
        else: 
            return make_response(
                jsonify (
                    message = "no course found"
                ), 404
            )

    def post(self):
        index = request.args.get('index')
        staff_email = request.args.get('staff_email')
        if (is_staff(staff_email) is False):
            return make_response(
                jsonify(
                    message = "Not staff - unauthorized access"
                ), 401
            )
        if (is_course(index)):
            return make_response(
                jsonify(
                    message = "Course already exist"
                ), 400
            )
        course = create_course(index)
        if (course):
            db.session.add(course)
            db.session.commit()
            return make_response(
                jsonify(
                    message = "Course creation - successful"
                ), 200
            )
        else:  
            return make_response(
                jsonify (
                    message = "Course creation - precondition failed"
                ), 412
            )