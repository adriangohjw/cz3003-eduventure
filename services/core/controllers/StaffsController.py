from flask import jsonify, request
from flask_restful import Resource

from models import User, Staff, Rs_staff_course_teach
from flask.helpers import make_response

from ..dao.StaffsDAO import staffRead
from ..contracts.staffs_contracts import staffReadContract, staffCreateContract
from ..operations.staffs_operations import staffReadOperation, staffCreateOperation
from exceptions import ErrorWithCode

class StaffAPI(Resource):
    def get(self):
        # contracts
        try:
            s = staffReadContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )
        
        # operations
        try:
            staff = staffReadOperation(s['email'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify (staff.asdict()), 200
        )

    def post(self):
        # contracts
        try:
            s = staffCreateContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            staff = staffCreateOperation(s['email'], s['password'], s['name'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify(staff.asdict()), 200
        )


from ..contracts.rs_staff_course_teaches_contracts import \
    courseMngReadContract, courseMngCreateContract
from ..operations.rs_staff_course_teaches_operations import \
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
            staff = courseMngReadOperation(s['user_email'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify (staff.asdict_courseMng()), 200
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
        