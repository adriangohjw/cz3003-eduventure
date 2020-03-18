from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.URI

    return app

if __name__ == "__main__":
    app = create_app()

    from models import db 
    db.init_app(app)

    from services.core.app import user_bp, staff_bp, student_bp, course_bp, topic_bp, lesson_bp
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(staff_bp, url_prefix='/staffs')
    app.register_blueprint(student_bp, url_prefix='/students')
    app.register_blueprint(course_bp, url_prefix='/courses')
    app.register_blueprint(topic_bp, url_prefix='/topics')
    app.register_blueprint(lesson_bp, url_prefix='/lessons')

    from services.quiz.app import quiz_bp, question_bp, questionchoice_bp
    app.register_blueprint(quiz_bp, url_prefix='/quizzes')
    app.register_blueprint(question_bp, url_prefix='/questions')
    app.register_blueprint(questionchoice_bp, url_prefix='/question_choices')

    app.run(port=5000, debug=True)