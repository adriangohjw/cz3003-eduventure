from flask import Flask
from config import ConfigTest
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ConfigTest.URI
    app.url_map.strict_slashes = False

    from services.core.blueprint import \
        user_bp, staff_bp, student_bp, course_bp, topic_bp, lesson_bp, \
        questionAttempt_bp, quizAttempt_bp, challenge_bp, progress_bp, statistics_bp

    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(staff_bp, url_prefix='/staffs')
    app.register_blueprint(student_bp, url_prefix='/students')
    app.register_blueprint(course_bp, url_prefix='/courses')
    app.register_blueprint(topic_bp, url_prefix='/topics')
    app.register_blueprint(lesson_bp, url_prefix='/lessons')
    app.register_blueprint(questionAttempt_bp, url_prefix='/question_attempts')
    app.register_blueprint(quizAttempt_bp, url_prefix='/quiz_attempts')
    app.register_blueprint(challenge_bp, url_prefix='/challenges')
    app.register_blueprint(progress_bp, url_prefix='/progresses')
    app.register_blueprint(statistics_bp, url_prefix='/statistics')

    from services.quiz.blueprint import \
        quiz_bp, question_bp, questionchoice_bp
        
    app.register_blueprint(quiz_bp, url_prefix='/quizzes')
    app.register_blueprint(question_bp, url_prefix='/questions')
    app.register_blueprint(questionchoice_bp, url_prefix='/question_choices')

    return app
