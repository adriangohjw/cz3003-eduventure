from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import Config

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = Config.URI
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

class Staff(User):
    __tablename__ = 'staffs'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

class Student(User):
    __tablename__ = 'students'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    matriculation_number = db.Column(db.String(255), unique=True, nullable=False)

class Course(db.Model):
    __tablename__ = 'courses'
    index = db.Column(db.String(255), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

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

class QuestionChoices(db.Model):
    __tablename__ = 'questionchoices'
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
if __name__ == '__main__':
    manager.run()