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
            student = studentCreateOperation(
                s['email'], s['password'], s['matriculation_number'], s['name']
            )
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

from ..contracts.rs_student_course_enrols_contracts import \
    courseMngReadContract, courseMngCreateContract
from ..operations.rs_student_course_enrols_operations import \
    courseMngReadOperation, courseMngCreateOperation

class CourseManagerAPI(Resource):
    def get(self):
        # contracts
        try:
            s = courseMngReadContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )
        
        # operations
        try:
            student = courseMngReadOperation(s['user_email'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify (student.asdict_courseMng()), 200
        )

    def post(self):
        # contracts
        try:
            r = courseMngCreateContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            rs = courseMngCreateOperation(r['user_email'], r['course_index'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify(rs.asdict()), 200
        )
