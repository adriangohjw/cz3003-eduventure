from flask import jsonify, request
from flask_restful import Resource

from models import db, Course, Staff
from flask.helpers import make_response

from ..dao.StaffsDAO import staffRead
from ..dao.CoursesDAO import courseCreate, courseRead

def initializeCourse(index):
    if (index is not None):
        return Course(index)
    else:
        return False

class CourseAPI(Resource):
    def get(self):
        index = request.args.get('index')
        course = courseRead(index)
        if (course):    # course exists        
            return make_response(
                jsonify (
                    message = "Course found"
                ), 200
            )
        else:   # course does not exist
            return make_response(
                jsonify (
                    message = "no course found"
                ), 404
            )

    def post(self):
        index = request.args.get('index')
        staff_email = request.args.get('staff_email')
        staff = staffRead(col='email', value=staff_email)
        course = initializeCourse(index)
        if (staff is False):    # email does not belong to staff
            return make_response(
                jsonify(
                    message = "Not staff - unauthorized access"
                ), 401
            )
        if (courseRead(index)):    # if course already exist
            return make_response(
                jsonify(
                    message = "Course already exist"
                ), 400
            )
        else:   # course does not exist yet
            course_create_status = courseCreate(course)
            if (course_create_status):    # if course creation is successful
                return make_response(
                    jsonify(
                        message = "Course creation - successful"
                    ), 200
                )
            else:   # if course creation is unsuccessful 
                return make_response(
                    jsonify (
                        message = "Course creation - precondition failed"
                    ), 412
                )