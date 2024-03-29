from flask import Blueprint
from flask_restful import Api

from services.core.controllers import \
    UsersController, StaffsController, StudentsController, \
    CoursesController, TopicsController, LessonsController, \
    QuestionAttemptsController, QuizAttemptsController, ChallengesController, \
    ProgressesController, StatisticsController

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
api_topic.add_resource(TopicsController.TopicListAPI, '/all')

lesson_bp = Blueprint('lesson', __name__)
api_lessons = Api(lesson_bp)
api_lessons.add_resource(LessonsController.LessonAPI, '/')
api_lessons.add_resource(LessonsController.LessonListAPI, '/all')
api_lessons.add_resource(LessonsController.QuizManagerAPI, '/quizzes')

questionAttempt_bp = Blueprint('questionAttempt', __name__)
api_questionAttempt = Api(questionAttempt_bp)
api_questionAttempt.add_resource(QuestionAttemptsController.QuestionAttemptAPI, '/')
api_questionAttempt.add_resource(QuestionAttemptsController.QuestionAttemptListAPI, '/list')

quizAttempt_bp = Blueprint('quizAttempt', __name__)
api_quizAttempt = Api(quizAttempt_bp)
api_quizAttempt.add_resource(QuizAttemptsController.QuizAttemptAPI, '/')
api_quizAttempt.add_resource(QuizAttemptsController.QuizAttemptListAPI, '/list')

challenge_bp = Blueprint('challenge', __name__)
api_challenges = Api(challenge_bp)
api_challenges.add_resource(ChallengesController.ChallengeAPI, '/')

progress_bp = Blueprint('progress', __name__)
api_progress = Api(progress_bp)
api_progress.add_resource(ProgressesController.ProgressAPI, '/')

statistics_bp = Blueprint('statistics', __name__)
api_statistics = Api(statistics_bp)
api_statistics.add_resource(StatisticsController.Stats_API, '/stat')
api_statistics.add_resource(StatisticsController.Lesson_Completion_API, '/lesson_completed')
api_statistics.add_resource(StatisticsController.LeaderBoard_API, '/leaderboard')
api_statistics.add_resource(StatisticsController.StudentScore_API, '/student_score')
api_statistics.add_resource(StatisticsController.CourseScore_API, '/course_score')
api_statistics.add_resource(StatisticsController.Activity_API, '/activity')
