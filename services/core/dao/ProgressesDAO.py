from sqlalchemy import asc, case
from sqlalchemy.sql.functions import count, coalesce, max

from models import \
    db, Topic, Lesson, Rs_lesson_quiz_contain, Quiz, Rs_quiz_question_contain, Question,\
    QuizAttempt


def progressRead(student_id):

    sq_attempts = \
        db.session.query(
            QuizAttempt.student_id,
            QuizAttempt.quiz_id,
            max(QuizAttempt.score).label('score')
        )\
        .filter_by(student_id=student_id)\
        .group_by(
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
            sq_attempts.c.student_id.label('sq_attempts_student_id'),
            coalesce(sq_attempts.c.score, 0).label('sq_attempts_score'),
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
            sq_attempts.c.student_id,
            sq_attempts.c.score
        )\
        .order_by(
            asc(Topic.id),
            asc(Lesson.id),
            asc(Quiz.id)
        )
        
    return query_results.all()
