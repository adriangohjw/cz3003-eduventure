from sqlalchemy import asc, desc, cast, Float, func, Numeric, Date, and_
from sqlalchemy.sql.functions import count, max

from models import \
    db, Topic, Lesson, Question, Quiz, Student, \
    Rs_lesson_quiz_contain, QuizAttempt, Rs_quiz_course_assign, Rs_quiz_question_contain, Rs_student_course_enrol

import datetime 


def statRead():

    relationships = Rs_lesson_quiz_contain.query.all()
    quizzes_list = [rs.quiz_id for rs in relationships]

    query = \
        db.session.query(
            Rs_quiz_course_assign.course_index.label('course_index'),
            Quiz.id.label('quiz_id'),
            Quiz.name.label('quiz_name'),
            Rs_student_course_enrol.student_id.label('student_id'),
            QuizAttempt.score.label('attempt_score'),
        )\
        .select_from(Rs_quiz_course_assign)\
        .outerjoin(Quiz, Quiz.id == Rs_quiz_course_assign.quiz_id)\
        .outerjoin(Rs_student_course_enrol, Rs_quiz_course_assign.course_index == Rs_student_course_enrol.course_index)\
        .outerjoin(QuizAttempt, and_(Quiz.id == QuizAttempt.quiz_id, Rs_student_course_enrol.student_id == QuizAttempt.student_id))\
        .filter(Quiz.id.in_(quizzes_list))\
        .order_by(
            asc(Rs_quiz_course_assign.course_index),
            asc(Quiz.id),
            asc(Rs_student_course_enrol.student_id) 
        )   

    return query.all()


def lessonCompletedRead():

    sq_attempts = \
        db.session.query(
            Rs_student_course_enrol.course_index.label('course_index'),
            QuizAttempt.student_id.label('student_id'),
            QuizAttempt.quiz_id.label('quiz_id'),
            max(QuizAttempt.score).label('score')
        )\
        .select_from(Rs_student_course_enrol)\
        .outerjoin(QuizAttempt, QuizAttempt.student_id == Rs_student_course_enrol.student_id)\
        .group_by(
            Rs_student_course_enrol.course_index,
            QuizAttempt.student_id,
            QuizAttempt.quiz_id
        )\
        .subquery()

    query_results = \
        db.session.query(
            Topic.id.label('topic_id'), 
            Topic.name.label('topic_name'), 
            Lesson.id.label('lesson_id'), 
            Lesson.name.label('lesson_name'),
            Quiz.id.label('quiz_id'),
            Quiz.name.label('quiz_name'),
            sq_attempts.c.course_index.label('course_index'),
            sq_attempts.c.student_id.label('student_id'),
            sq_attempts.c.score.label('score'),
            count(Question.id).label('count_questions')
        )\
        .select_from(Topic)\
        .outerjoin(Lesson)\
        .outerjoin(Rs_lesson_quiz_contain)\
        .outerjoin(Quiz)\
        .outerjoin(sq_attempts, Quiz.id == sq_attempts.c.quiz_id)\
        .outerjoin(Rs_quiz_question_contain)\
        .outerjoin(Question)\
        .group_by(
            Topic.id, 
            Topic.name, 
            Lesson.id,
            Lesson.name,
            Quiz.id,
            Quiz.name,
            sq_attempts.c.course_index,
            sq_attempts.c.student_id,
            sq_attempts.c.score
        )\
        .order_by(
            asc(Topic.id),
            asc(Lesson.id),
            asc(Quiz.id),
            asc(sq_attempts.c.course_index),
            asc(sq_attempts.c.student_id)
        )
        
    return query_results.all()


def leaderboardRead():

    query_results = \
        db.session.query(
            QuizAttempt.student_id.label('student_id'),
            Student.name.label('student_name'),
            Student.matriculation_number.label('student_matriculation_num'),
            QuizAttempt.quiz_id.label('quiz_id'),
            QuizAttempt.score.label('score')
        )\
        .select_from(QuizAttempt)\
        .outerjoin(Student, QuizAttempt.student_id == Student.id)\
        .order_by(
            asc(QuizAttempt.student_id),
            asc(QuizAttempt.quiz_id),
            desc(QuizAttempt.created_at)
        )
    
    return query_results.all()


def studentScoreRead():

    query_results = \
        db.session.query(
            QuizAttempt.student_id.label('student_id'),
            Student.name.label('student_name'),
            QuizAttempt.quiz_id.label('quiz_id'),
            Quiz.name.label('quiz_name'),
            QuizAttempt.score.label('score')
        )\
        .select_from(QuizAttempt)\
        .outerjoin(Student, QuizAttempt.student_id == Student.id)\
        .outerjoin(Quiz, QuizAttempt.quiz_id == Quiz.id)\
        .order_by(
            asc(QuizAttempt.student_id),
            asc(QuizAttempt.quiz_id),
            desc(QuizAttempt.created_at)
        )
    
    return query_results.all()


def courseScoreRead():

    relationships = Rs_lesson_quiz_contain.query.all()
    quiz_list = [item.quiz_id for item in relationships]
    quiz_list = list(set(quiz_list))

    query_results = \
        db.session.query(
            Rs_student_course_enrol.course_index.label('course_index'),
            QuizAttempt.student_id.label('student_id'),
            QuizAttempt.quiz_id.label('quiz_id'),
            func.round(
                cast(100 * cast(QuizAttempt.score, Float) / cast(count(Question.id), Float), Numeric), 
                0
            ).label('quiz_score_percentage')
        )\
        .select_from(QuizAttempt)\
        .outerjoin(Rs_student_course_enrol, QuizAttempt.student_id == Rs_student_course_enrol.student_id)\
        .outerjoin(Rs_quiz_question_contain, QuizAttempt.quiz_id == Rs_quiz_question_contain.quiz_id)\
        .outerjoin(Question, Rs_quiz_question_contain.question_id == Question.id)\
        .filter(QuizAttempt.quiz_id.in_(quiz_list))\
        .group_by(
            Rs_student_course_enrol.course_index,
            QuizAttempt.student_id, 
            QuizAttempt.quiz_id,
            QuizAttempt.score
        )\
        .order_by(
            asc(QuizAttempt.student_id)
        )

    return query_results.all()


def activityRead(date_start, date_end, student_id):

    query_results = \
        db.session.query(
            cast(QuizAttempt.created_at, Date).label('created_at'),
            QuizAttempt.quiz_id.label('quiz_id')
        )\
        .filter(QuizAttempt.student_id == student_id)\
        .filter(QuizAttempt.created_at >= date_start - datetime.timedelta(days=1))\
        .filter(QuizAttempt.created_at <= date_end + datetime.timedelta(days=1))\
        .order_by(
            asc(QuizAttempt.created_at)
        )

    return query_results.all() 
