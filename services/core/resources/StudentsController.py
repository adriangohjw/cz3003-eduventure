from flask import jsonify, request
from flask_restful import Resource

from models import Rs_student_course_enrol, Student, User, db
from flask.helpers import make_response

from .UsersController import initializeUser
from ..dao.UsersDAO import userRead
from ..dao.StudentsDAO import studentCreate, studentRead, studentUpdate

def initializeStudent(email, password, matriculation_number):
    user = initializeUser(email, password)
    if (user and (matriculation_number is not None)):
        return Student(user, matriculation_number)
    else:
        return False

class StudentAPI(Resource):
    def get(self):
        email = request.args.get('email')
        student = studentRead(col='email', value=email)
        if (student):   # if student exist
            return make_response(
                jsonify(
                    message = "User is Student",
                    matriculation_number = student.matriculation_number
                ), 200
            )
        else:   # if student does not exist or that user is not a student
            return make_response(
                jsonify(
                    message = "User is not student / does not exist"
                ), 404
            )

    def post(self):
        email = request.args.get('email')
        password = request.args.get('password')
        matriculation_number = request.args.get('matriculation_number')
        student = initializeStudent(email, password, matriculation_number)
        if (studentRead(col='email', value=student.email)): # if existing student
            return make_response(
                jsonify (
                    message = "Student {} already exist".format(student.email)
                ), 409
            )
        else:
            student_create_status = studentCreate(student)
            if (student_create_status): # if student creation is successful
                return make_response(
                    jsonify(
                        message = "Student creation - successful"
                    ), 200
                )
            else:    # if student creation is unsuccessful
                return make_response(
                    jsonify (
                        message = "Student creation - precondition failed"
                    ), 412
                )


from .CoursesController import is_course
from ..dao.StudentsDAO import courseMngCreate, courseMngRead

def initializeRsStudentCourseEnrol(student_id, course_index):
    if ((student_id is not None) and (course_index is not None)):
        return Rs_student_course_enrol(student_id, course_index)
    else:
        return False

class CourseManagerAPI(Resource):
    def get(self):
        user_email = request.args.get('user_email')
        student = studentRead(col='email', value=user_email)
        if (student):   # if rs between student and course found
            return make_response(
                jsonify(
                    message = "Student and courses found",
                    count_courses = len(student.rs_student_course_enrols),
                    course = student.rs_student_course_enrols
                )
            )
        else:   # if rs between student and course not found
            return make_response(
                jsonify(
                    message = "User is not student / does not exist"
                ), 404
            )
    
    def post(self):
        user_email = request.args.get('user_email')
        course_index = request.args.get('course_index')    
        student = studentRead(col='email', value=user_email)
        rs = courseMngRead(student_id=student.id, course_index=course_index)
        if (rs):    # rs already exist
            return make_response(
                jsonify(
                    message = "Relationship already exist"
                ), 409
            )
        else:   # rs does not exist yet
            rs = initializeRsStudentCourseEnrol(student_id=student.id, course_index=course_index)
            rs_create_status = courseMngCreate(rs)
            if (rs_create_status):  # successful in adding Rs to DB
                return make_response(
                    jsonify(
                        message = "Relationship added"
                    ), 200
                )
            else:   # unsuccessful in adding Rs to DB
                return make_response(
                    jsonify(
                        message = "Relationship not added - failed precondition"
                    ), 412
                )