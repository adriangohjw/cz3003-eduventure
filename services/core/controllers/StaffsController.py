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
            staff = staffCreateOperation(s['email'], s['password'])
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


from ..dao.CoursesDAO import courseRead
from ..dao.StaffsDAO import courseMngCreate, courseMngRead

def initializeRsStaffCourseTeach(staff_id, course_index):
    if ((staff_id is not None) and (course_index is not None)):
        return Rs_staff_course_teach(staff_id, course_index)
    else:
        return False

class CourseManagerAPI(Resource):
    def get(self):
        user_email = request.args.get('user_email')
        staff = staffRead(col='email', value=user_email)
        if (staff): # if rs between staff and course found
            return make_response(
                jsonify(
                    message = "Staff and courses found",
                    count_courses = len(staff.rs_staff_course_teaches),
                    course = staff.rs_staff_course_teaches
                )
            )
        else:   # if rs between staff and course not found
            return make_response(
                jsonify(
                    message = "User is not staff / does not exist"
                ), 404
            )
    
    def post(self):
        user_email = request.args.get('user_email')
        course_index = request.args.get('course_index')
        staff = staffRead(col='email', value=user_email)
        course = courseRead(course_index)
        rs = courseMngRead(staff_id=staff.id, course_index=course.index)
        if (rs):    # rs already exist
            return make_response(
                jsonify(
                    message = "Relationship already exist"
                ), 409
            )
        else:   # rs does not exist yet
            rs = initializeRsStaffCourseTeach(staff_id=staff.id, course_index=course.index)
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