from flask import Blueprint
from flask_restful import Resource, Api
from config import Config

from services.core.resources import \
    UsersController, StaffsController, StudentsController, \
    CoursesController, TopicsController, LessonsController

user_bp = Blueprint('user', __name__)
api_user = Api(user_bp)
api_user.add_resource(UsersController.UserAPI, '/')

staff_bp = Blueprint('staff', __name__)
api_staff = Api(staff_bp)
api_staff.add_resource(StaffsController.StaffAPI, '/')
api_staff.add_resource(StaffsController.CourseManagerAPI, '/courses')

student_bp = Blueprint('student', __name__)
api_student = Api(student_bp)
api_student.add_resource(StudentsController.StudentAPI, '/')
api_student.add_resource(StudentsController.CourseManagerAPI, '/courses')

course_bp = Blueprint('course', __name__)
api_course = Api(course_bp)
api_course.add_resource(CoursesController.CourseAPI, '/')

topic_bp = Blueprint('topic', __name__)
api_topic = Api(topic_bp)
api_topic.add_resource(TopicsController.TopicAPI, '/')

lesson_bp = Blueprint('lesson', __name__)
api_lesosn = Api(lesson_bp)
api_lesosn.add_resource(LessonsController.LessonAPI, '/')