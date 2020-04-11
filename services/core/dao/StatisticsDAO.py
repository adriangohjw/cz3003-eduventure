from sqlalchemy import asc, case

from models import \
    db, Rs_lesson_quiz_contain, Quiz, QuizAttempt, Rs_quiz_course_assign


def statRead():

    relationships = Rs_lesson_quiz_contain.query.all()
    quizzes_list = [rs.quiz_id for rs in relationships]

    return \
        db.session.query(
            Rs_quiz_course_assign.course_index.label('course_index'),
            Quiz.id.label('quiz_id'),
            Quiz.name.label('quiz_name'),
            QuizAttempt.score.label('attempt_score'),
        )\
        .select_from(Rs_quiz_course_assign)\
        .outerjoin(Quiz)\
        .outerjoin(QuizAttempt)\
        .filter(Quiz.id.in_(quizzes_list))\
        .order_by(
            asc(Quiz.id)
        )\
        .all()
