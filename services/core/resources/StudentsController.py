from flask import jsonify, request
from flask_restful import Resource

from models import Rs_student_course_enrol, Student, User, db
from flask.helpers import make_response

import requests

from .UsersController import is_existing, create_user

def is_student(col, value):
    if (col == 'email'):
        user = User.query.filter_by(email=value).first()
        return bool(Student.query.filter_by(id=user.id).first())
    if (col == 'id'):
        return bool(Student.query.filter_by(id=value).first())

def getStudent(col, value):
    if (is_student(col=col, value=value)):
        if (col == 'email'):
            return Student.query.filter_by(email=value).first()
        elif (col == 'id'):
            return Student.query.filter_by(id=value).first()
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


from .CoursesController import is_course

class CourseManagerAPI(Resource):
    def get(self):
        user_email = request.args.get('user_email')
        student = getStudent(col='email', value=user_email)
        if (student):
            return make_response(
                jsonify(
                    message = "Student and courses found",
                    count_courses = len(student.rs_student_course_enrols),
                    course = student.rs_student_course_enrols
                )
            )
        else:
            return make_response(
                jsonify(
                    message = "User is not student / does not exist"
                ), 404
            )
    
    def post(self):
        user_email = request.args.get('user_email')
        course_index = request.args.get('course_index')    
        student = getStudent(col='email', value=user_email)
        if (student and is_course(index=course_index)):
            rs = Rs_student_course_enrol.query.filter_by(student_id=student.id).filter_by(course_index=course_index).first()
            if (bool(rs)):
                return make_response(
                    jsonify(
                        message = "Relationship already exist"
                    ), 409
                )
            else:
                rs = Rs_student_course_enrol(student_id=student.id, course_index=course_index)
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