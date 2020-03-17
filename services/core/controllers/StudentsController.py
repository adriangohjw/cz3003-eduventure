from flask import jsonify, request
from flask_restful import Resource

from models import Rs_student_course_enrol
from flask.helpers import make_response

from ..dao.StudentsDAO import studentRead
from ..contracts.students_contracts import studentReadContract, studentCreateContract
from ..operations.students_operations import studentReadOperation, studentCreateOperation

from exceptions import ErrorWithCode

class StudentAPI(Resource):
    def get(self):
        # contracts
        try:
            s = studentReadContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )
        
        # operations
        try:
            student = studentReadOperation(s['email'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify (student.asdict()), 200
        )

    def post(self):
        # contracts
        try:
            s = studentCreateContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            student = studentCreateOperation(s['email'], s['password'], s['matriculation_number'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify(student.asdict()), 200
        )


from ..dao.CoursesDAO import courseRead
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
        course = courseRead(course_index)
        rs = courseMngRead(student_id=student.id, course_index=course.index)
        if (rs):    # rs already exist
            return make_response(
                jsonify(
                    message = "Relationship already exist"
                ), 409
            )
        else:   # rs does not exist yet
            rs = initializeRsStudentCourseEnrol(student_id=student.id, course_index=course.index)
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