from flask import jsonify, request
from flask_restful import Resource
from flask.helpers import make_response

from exceptions import ErrorWithCode

from ..contracts.courses_contracts import courseReadContract, courseCreateContract
from ..operations.courses_operations import courseReadOperation, courseCreateOperation

class CourseAPI(Resource):
    def get(self):
        # contracts
        try:
            c = courseReadContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )
        
        # operations
        try:
            course = courseReadOperation(c['index'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify (course.asdict()), 200
        )

    def post(self):
        # contracts
        try:
            c = courseCreateContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            course = courseCreateOperation(c['index'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify(course.asdict()), 200
        )

from services.core.contracts.rs_student_course_enrols_contracts import courseClasslistReadContract
from services.core.operations.rs_student_course_enrols_operations import courseClasslistReadOperation

class CourseClasslistAPI(Resource):
    def get(self):
        # contracts
        try:
            c = courseClasslistReadContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )
        
        # operations
        try:
            relationships = courseClasslistReadOperation(c['course_index'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        students_list = []
        for rs in relationships:
            students_list.append(
                {
                    'id': rs.student.id,
                    'email': rs.student.email, 
                    'name': rs.student.name
                }
            )
        return make_response(
            jsonify (
                students = students_list
            ), 200
        )
