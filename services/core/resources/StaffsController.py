from flask import jsonify, request
from flask_restful import Resource

from models import db, User, Staff, Course, Rs_staff_course_teach
from flask.helpers import make_response

import requests

from .UsersController import initializeUser
from ..dao.UsersDAO import userRead

def is_staff(col, value):
    if (col == 'email'):
        user = User.query.filter_by(email=value).first()
        return bool(Staff.query.filter_by(id=user.id).first())
    if (col == 'id'):
        return bool(Staff.query.filter_by(id=value).first())

def getStaff(col, value):
    if (is_staff(col=col, value=value)):
        if (col == 'email'):
            return Staff.query.filter_by(email=value).first()
        elif (col == 'id'):
            return Staff.query.filter_by(id=value).first()
    else:
        return False

class StaffAPI(Resource):
    def get(self):
        email = request.args.get('email')
        if (is_staff(col='email', value=email)):
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
        if (userRead(col='email', value=email)):
            return make_response(
                jsonify(
                    message = "Staff already exist"
                ), 400
            )
        password = request.args.get('password')
        user = initializeUser(email, password)
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


from .CoursesController import is_course

class CourseManagerAPI(Resource):
    def get(self):
        user_email = request.args.get('user_email')
        staff = getStaff(col='email', value=user_email)
        if (staff):
            return make_response(
                jsonify(
                    message = "Staff and courses found",
                    count_courses = len(staff.rs_staff_course_teaches),
                    course = staff.rs_staff_course_teaches
                )
            )
        else:
            return make_response(
                jsonify(
                    message = "User is not staff / does not exist"
                ), 404
            )
    
    def post(self):
        user_email = request.args.get('user_email')
        course_index = request.args.get('course_index')
        staff = getStaff(col='email', value=user_email)
        if (staff and is_course(index=course_index)):
            rs = Rs_staff_course_teach.query.filter_by(staff_id=staff.id).filter_by(course_index=course_index).first()
            if (bool(rs)):
                return make_response(
                    jsonify(
                        message = "Relationship already exist"
                    ), 409
                )
            else:
                rs = Rs_staff_course_teach(staff_id=staff.id, course_index=course_index)
                db.session.add(rs)
                db.session.commit()
                return make_response(
                    jsonify(
                        message = "Relationship added"
                    ), 200
                )
        else:
            return make_response(
                jsonify(
                    message = "Relationship not added - failed precondition"
                ), 412
            )