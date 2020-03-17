from flask import jsonify, request
from flask_restful import Resource

from models import Course, Staff
from flask.helpers import make_response

from ..contracts.courses_contracts import courseReadContract, courseCreateContract
from ..operations.courses_operations import courseReadOperation, courseCreateOperation
from exceptions import ErrorWithCode

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
