from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

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

    def asdict(self):
        return {
            'id': self.id,
            'email': self.email,
            'encrypted_password': self.encrypted_password,
            'name': self.name,
            'created_at': self.created_at,
        }

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

    def asdict(self):
        return {
            'id': self.id,
            'email': self.email,
            'encrypted_password': self.encrypted_password,
            'name': self.name,
            'created_at': self.created_at,
            'count_quizzes': len(self.quizzes),
            'quizzes': [q.to_json() for q in self.quizzes]
        }

    def asdict_courseMng(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'count_courses': len(self.courses),
            'courses': [c.to_json() for c in self.courses],
            'quizzes': [q.asdict() for q in self.quizzes]
        }

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

    def asdict(self):
        return {
            'id': self.id,
            'email': self.email,
            'encrypted_password': self.encrypted_password,
            'name': self.name,
            'created_at': self.created_at,
            'matriculation_number': self.matriculation_number
        }

    def asdict_courseMng(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'count_courses': len(self.courses),
            'courses': [c.to_json() for c in self.courses]
        }

class Course(db.Model):
    __tablename__ = 'courses'
    index = db.Column(db.String(255), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, index):
        self.index = index
        
    def asdict(self):
        return {
            'index': self.index,
            'created_at': self.created_at
        }

class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    lessons = db.relationship('Lesson', backref='topic')

    def __init__(self, name):
        self.name = name

    def asdict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at
        }

class Lesson(db.Model):
    __tablename__ = 'lessons'
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), primary_key=True)
    id = db.Column(db.Integer, primary_key=True, nullable=True)
    name = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    url_link = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    questions = db.relationship('Question', backref='lesson')

    def __init__(self, topic_id, id, name, content, url_link=None):
        self.topic_id = topic_id
        self.id = id
        self.name = name
        self.content = content  
        self.url_link = url_link

    def asdict(self):
        return {
            'topic_id': self.topic_id,
            'id': self.id,
            'name': self.name,
            'content': self.content,
            'url_link': self.url_link,
            'created_at': self.created_at,
            'count_questions': len(self.questions),
            'questions': [q.asdict() for q in self.questions]
        }
    
class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer)
    lesson_id = db.Column(db.Integer)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    __table_args__ = (db.ForeignKeyConstraint([topic_id, lesson_id], [Lesson.topic_id, Lesson.id]),{})
    choices = db.relationship('QuestionChoice', backref='question')
    attempts = db.relationship('QuestionAttempt', backref='question')

    def __init__(self, topic_id, lesson_id, description):
        self.topic_id = topic_id
        self.lesson_id = lesson_id
        self.description = description

    def asdict(self):
        return {
            'id': self.id,
            'topic_id': self.topic_id,
            'lesson_id': self.lesson_id,
            'description': self.description,
            'created_at': self.created_at,
            'count_choices': len(self.choices),
            'choices': [z.to_json() for z in self.choices],
            'count_attempts': len(self.attempts),
            'attempts': [qa.asdict() for qa in self.attempts]
        }

class QuestionChoice(db.Model):
    __tablename__ = 'questionchoices'
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, question_id, id, description, is_correct):
        self.question_id = question_id
        self.id = id
        self.description = description
        self.is_correct = is_correct

    def asdict(self):
        return {
            'question_id': self.question_id,
            'id': self.id,
            'description': self.description,
            'is_correct': self.is_correct,
            'created_at': self.created_at
        }

    def to_json(self):
        return {
            'id': self.id,
            'description': self.description,
            'is_correct': self.is_correct,
            'created_at': self.created_at
        }

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
    challenges = db.relationship('Challenge', backref='quiz')

    def __init__(self, staff_id, name, is_fast, date_start, date_end):
        self.name = name
        self.staff_id = staff_id
        self.is_fast = is_fast
        self.date_start = date_start
        self.date_end = date_end

    def asdict(self):
        return {
            'id': self.id,
            'name': self.name,
            'staff': {
                'id': self.staff_id,
                'name': self.staff.name
            },
            'is_fast': self.is_fast,
            'date_start': self.date_start,
            'date_end': self.date_end,
            'attempts': [qa.asdict() for qa in self.attempts]
        }

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'is_fast': self.is_fast,
            'date_start': self.date_start,
            'date_end': self.date_end,
            'created_at': self.created_at
        }

    def asdict_courseMng(self):
        return {
            'id': self.id,
            'staff_id': self.staff_id,
            'name': self.name,
            'is_fast': self.is_fast,
            'date_start': self.date_start,
            'date_end': self.date_end,
            'count_attempts': len(self.attempts),
            'count_courses': len(self.courses),
            'courses': [c.asdict() for c in self.courses]
        }

    def asdict_questionMng(self):
        return {
            'id': self.id,
            'staff_id': self.staff_id,
            'name': self.name,
            'is_fast': self.is_fast,
            'date_start': self.date_start,
            'date_end': self.date_end,
            'count_attempts': len(self.attempts),
            'count_questions': len(self.questions),
            'questions': [q.asdict_getQuestion() for q in self.questions]
        }

class QuestionAttempt(db.Model):
    __tablename__ = 'questionattempts'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    duration_ms = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, student_id, question_id, is_correct, duration_ms):
        self.student_id = student_id
        self.question_id = question_id
        self.is_correct = is_correct
        self.duration_ms = duration_ms

    def asdict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'question_id': self.question_id,
            'is_correct': self.is_correct,
            'duration_ms': self.duration_ms,
            'created_at': self.created_at
        }

class QuizAttempt(db.Model):
    __tablename__ = 'quizattempts'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))
    score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, student_id, quiz_id, score):
        self.student_id = student_id
        self.quiz_id = quiz_id
        self.score = score

    def asdict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'quiz_id': self.quiz_id,
            'score': self.score,
            'created_at': self.created_at
        }

class Challenge(db.Model):
    __tablename__ = 'challenges'
    from_student_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)
    to_student_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), primary_key=True)
    winner_id = db.Column(db.Integer)
    is_completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    __table_args__ = (
        db.UniqueConstraint('from_student_id', 'to_student_id', 'quiz_id'),
    )
    from_person = db.relationship('Student', backref='challenge_received', foreign_keys=[from_student_id])
    to_person = db.relationship('Student', backref='challenge_sent', foreign_keys=[to_student_id])

    def __init__(self, from_student_id, to_student_id, quiz_id):
        self.from_student_id = from_student_id
        self.to_student_id = to_student_id
        self.quiz_id = quiz_id
        self.winner_id = None

    def asdict(self):
        return {
            'from_student_id': self.from_student_id,
            'to_student_id': self.to_student_id,
            'quiz_id': self.quiz_id,
            'is_completed': self.is_completed,
            'winner_id': self.winner_id,
            'created_at': self.created_at
        }

class Rs_staff_course_teach(db.Model):
    __tablename__ = 'rs_staff_course_teaches'
    staff_id = db.Column(db.Integer, db.ForeignKey('staffs.id'), primary_key=True)
    course_index = db.Column(db.String(255), db.ForeignKey('courses.index'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    staff = db.relationship('Staff', backref=db.backref('courses', cascade="all, delete-orphan"))
    course = db.relationship('Course', backref=db.backref('staffs', cascade="all, delete-orphan"))

    def __init__(self, staff_id, course_index):
        self.staff_id = staff_id
        self.course_index = course_index

    def asdict(self):
        return {
           'staff_id': self.staff_id,
           'course_index': self.course_index,
           'created_at': self.created_at 
        }
    
    def to_json(self):
        return {
            'course_index': self.course_index,
            'created_at': self.created_at
        }

class Rs_student_course_enrol(db.Model):
    __tablename__ = 'rs_student_course_enrols'
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)
    course_index = db.Column(db.String(255), db.ForeignKey('courses.index'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    student = db.relationship('Student', backref=db.backref('courses', cascade="all, delete-orphan"))
    course = db.relationship('Course', backref=db.backref('students', cascade="all, delete-orphan"))

    def __init__(self, student_id, course_index):
        self.student_id = student_id
        self.course_index = course_index

    def asdict(self):
        return {
           'student_id': self.student_id,
           'course_index': self.course_index,
           'created_at': self.created_at 
        }

    def to_json(self):
        return {
            'course_index': self.course_index,
            'created_at': self.created_at
        }

class Rs_quiz_course_assign(db.Model):
    __tablename__ = 'rs_quiz_course_assigns'
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), primary_key=True)
    course_index = db.Column(db.String(255), db.ForeignKey('courses.index'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    quiz = db.relationship('Quiz', backref=db.backref('courses', cascade="all, delete-orphan"))
    course = db.relationship('Course', backref=db.backref('quizzes', cascade="all, delete-orphan"))

    def __init__(self, quiz_id, course_index):
        self.quiz_id = quiz_id 
        self.course_index = course_index

    def asdict(self):
        return {
            'quiz_id': self.quiz_id,
            'course_index': self.course_index,
            'created_at': self.created_at 
        }

class Rs_quiz_question_contain(db.Model):
    __tablename__ = 'rs_quiz_question_contains'
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    quiz = db.relationship('Quiz', backref=db.backref('questions', cascade="all, delete-orphan"))
    question = db.relationship('Question', backref=db.backref('quizzes', cascade="all, delete-orphan"))

    def __init__(self, quiz_id, question_id):
        self.quiz_id = quiz_id 
        self.question_id = question_id

    def asdict(self):
        return {
            'quiz_id': self.quiz_id,
            'question_id': self.question_id,
            'created_at': self.created_at 
        }

    def asdict_getQuestion(self):
        return {
            'question': self.question.asdict(),
            'created_at': self.created_at
        }

class Rs_lesson_quiz_contain(db.Model):
    __tablename__ = 'rs_lesson_quiz_contains'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    topic_id = db.Column(db.Integer)
    lesson_id = db.Column(db.Integer)
    quiz_id = db.Column(db.Integer)
    __table_args__ = (
        db.ForeignKeyConstraint(
            [topic_id, lesson_id], 
            [Lesson.topic_id, Lesson.id]
        ),
    )
    __table_args__ = (
        db.ForeignKeyConstraint(
            [quiz_id], 
            [Quiz.id]
        ),
    )
    __table_args__ = (
        db.UniqueConstraint('topic_id', 'lesson_id', 'quiz_id'),
    )
    created_at = db.Column(db.DateTime, default=datetime.now)
    quiz = db.relationship('Quiz', backref=db.backref('lessons', cascade="all, delete-orphan"))
    lesson = db.relationship('Lesson', backref=db.backref('quizzes', cascade="all, delete-orphan"))

    def __init__(self, topic_id, lesson_id, quiz_id):
        self.topic_id = topic_id
        self.lesson_id = lesson_id
        self.quiz_id = quiz_id 

    def asdict(self):
        return {
            'id': self.id,
            'topic_id': self.topic_id,
            'lesson_id': self.lesson_id,
            'quiz_id': self.quiz_id,
            'created_at': self.created_at
        }

    def asdict_quizMng(self):
        return {
            'quiz_id': self.quiz_id
        }
