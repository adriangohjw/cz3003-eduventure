from flask import jsonify, request
from flask_restful import Resource

from models import User, Staff, Course, Rs_staff_course_teach
from flask.helpers import make_response

from .UsersController import initializeUser
from ..dao.UsersDAO import userRead
from ..dao.StaffsDAO import staffCreate, staffRead, staffUpdate

def initializeStaff(email, password):
    user = initializeUser(email, password)
    if (user):
        return Staff(email, password)
    else:
        return False

class StaffAPI(Resource):
    def get(self):
        email = request.args.get('email')
        staff = staffRead(col='email', value=email)
        if (staff): # if staff exist
            return make_response(
                jsonify(
                    message = "User is staff"
                ), 200
            )
        else:   # if staff does not exist or that user is not a staff
            return make_response(
                jsonify(
                    message = "User is not staff / does not exist"
                ), 404
            )

    def post(self):
        email = request.args.get('email')
        password = request.args.get('password')
        staff = initializeStaff(email, password)
        if (staffRead(col='email', value=email)):   # if existing staff
            return make_response(
                jsonify(
                    message = "Staff already exist"
                ), 400
            )
        else:
            staff_create_status = staffCreate(staff)
            if (staff_create_status):   # if staff creation is successful
                return make_response(
                    jsonify(
                        message = "Staff creation - successful"
                    ), 200
                )
            else:   # if staff creation is unsuccessful
                return make_response(
                    jsonify (
                        message = "Staff creation - precondition failed"
                    ), 412
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