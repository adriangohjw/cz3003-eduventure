from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import Config
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy.ext.hybrid import hybrid_property

from run import create_app
app = create_app()

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    encrypted_password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, email, encrypted_password, name):
        self.email = email 
        self.encrypted_password = encrypted_password
        self.name = name

    def get_encrypted_password(self):
        return self.encrypted_password

    def set_encrypted_password(self, encrypted_password):
        self.encrypted_password = encrypted_password

class Staff(User):
    __tablename__ = 'staffs'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    quizzes = db.relationship('Quiz', backref='staff')

    def __init__(self, user):
        self.email = user.email
        self.encrypted_password = user.encrypted_password
        self.name = user.name

class Student(User):
    __tablename__ = 'students'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    matriculation_number = db.Column(db.String(255), unique=True, nullable=False)
    questions_attempts = db.relationship('QuestionAttempt', backref='student')
    quiz_attempts = db.relationship('QuizAttempt', backref='student')

    def __init__(self, user, matriculation_number):
        self.email = user.email
        self.encrypted_password = user.encrypted_password
        self.name = user.name
        self.matriculation_number = matriculation_number

class Course(db.Model):
    __tablename__ = 'courses'
    index = db.Column(db.String(255), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, index):
        self.index = index

class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    lessons = db.relationship('Lesson', backref='topic')

class Lesson(db.Model):
    __tablename__ = 'lessons'
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    questions = db.relationship('Question', backref='lesson')
    
class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer)
    lesson_id = db.Column(db.Integer)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    __table_args__ = (db.ForeignKeyConstraint([topic_id, lesson_id], [Lesson.topic_id, Lesson.id]),{})
    choices = db.relationship('QuestionChoices', backref='question')
    attempts = db.relationship('QuestionAttempt', backref='question')

class QuestionChoices(db.Model):
    __tablename__ = 'questionchoices'
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staffs.id'))
    name = db.Column(db.String(255), nullable=False)
    is_fast = db.Column(db.Boolean, nullable=False)
    date_start = db.Column(db.Date, nullable=False)
    date_end = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    attempts = db.relationship('QuizAttempt', backref='quiz')

class QuestionAttempt(db.Model):
    __tablename__ = 'questionattempts'
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)
    is_correct = db.Column(db.Boolean, nullable=False)
    duration = db.Column(db.Interval)
    created_at = db.Column(db.DateTime, default=datetime.now)

class QuizAttempt(db.Model):
    __tablename__ = 'quizattempts'
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

class Rs_staff_course_teach(db.Model):
    __tablename__ = 'rs_staff_course_teaches'
    staff_id = db.Column(db.Integer, db.ForeignKey('staffs.id'), primary_key=True)
    course_index = db.Column(db.String(255), db.ForeignKey('courses.index'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    staff = db.relationship('Staff', backref=db.backref('rs_staff_course_teaches', cascade="all, delete-orphan"))
    course = db.relationship('Course', backref=db.backref('rs_staff_course_teaches', cascade="all, delete-orphan"))

class Rs_student_course_enrol(db.Model):
    __tablename__ = 'rs_student_course_enrols'
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)
    course_index = db.Column(db.String(255), db.ForeignKey('courses.index'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    student = db.relationship('Student', backref=db.backref('rs_student_course_enrols', cascade="all, delete-orphan"))
    course = db.relationship('Course', backref=db.backref('rs_student_course_enrols', cascade="all, delete-orphan"))

class Rs_quiz_course_assign(db.Model):
    __tablename__ = 'rs_quiz_course_assigns'
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), primary_key=True)
    course_index = db.Column(db.String(255), db.ForeignKey('courses.index'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    quiz = db.relationship('Quiz', backref=db.backref('rs_quiz_course_assigns', cascade="all, delete-orphan"))
    course = db.relationship('Course', backref=db.backref('rs_quiz_course_assigns', cascade="all, delete-orphan"))

class Rs_quiz_question_contain(db.Model):
    __tablename__ = 'rs_quiz_question_contains'
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    quiz = db.relationship('Quiz', backref=db.backref('rs_quiz_question_contains', cascade="all, delete-orphan"))
    question = db.relationship('Question', backref=db.backref('rs_quiz_question_contains', cascade="all, delete-orphan"))

if __name__ == '__main__':
    manager.run()