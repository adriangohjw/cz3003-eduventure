from flask import Blueprint
from flask_restful import Api

from services.core.controllers import \
    UsersController, StaffsController, StudentsController, \
    CoursesController, TopicsController, LessonsController, \
    QuestionAttemptsController, QuizAttemptsController, ChallengesController

user_bp = Blueprint('user', __name__)
api_user = Api(user_bp)
api_user.add_resource(UsersController.UserAPI, '/')
api_user.add_resource(UsersController.AuthenticationAPI, '/auth')

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
api_course.add_resource(CoursesController.CourseClasslistAPI, '/students/all')

topic_bp = Blueprint('topic', __name__)
api_topic = Api(topic_bp)
api_topic.add_resource(TopicsController.TopicAPI, '/')

lesson_bp = Blueprint('lesson', __name__)
api_lessons = Api(lesson_bp)
api_lessons.add_resource(LessonsController.LessonAPI, '/')
api_lessons.add_resource(LessonsController.QuizManagerAPI, '/quizzes')

questionAttempt_bp = Blueprint('questionAttempt', __name__)
api_questionAttempt = Api(questionAttempt_bp)
api_questionAttempt.add_resource(QuestionAttemptsController.QuestionAttemptAPI, '/')
api_questionAttempt.add_resource(QuestionAttemptsController.QuestionAttemptListAPI, '/list')
api_questionAttempt.add_resource(QuestionAttemptsController.QuestionAttemptLeaderboardAPI, '/leaderboard')

quizAttempt_bp = Blueprint('quizAttempt', __name__)
api_quizAttempt = Api(quizAttempt_bp)
api_quizAttempt.add_resource(QuizAttemptsController.QuizAttemptAPI, '/')
api_quizAttempt.add_resource(QuizAttemptsController.QuizAttemptListAPI, '/list')
api_quizAttempt.add_resource(QuizAttemptsController.QuizAttemptLeaderboardAPI, '/leaderboard')

challenge_bp = Blueprint('challenge', __name__)
api_challenges = Api(challenge_bp)
api_challenges.add_resource(ChallengesController.ChallengeAPI, '/')
