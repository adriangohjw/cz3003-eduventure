from models import db, QuizAttempt, Student
from sqlalchemy import func

def quizAttemptCreate(quizAttempt):
    db.session.add(quizAttempt)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def quizAttemptListRead(student_id, quiz_id):
    return QuizAttempt.query.\
        filter_by(student_id=student_id).filter_by(quiz_id=quiz_id).all()

def quizAttemptLeaderboardRead():
    return db.session.query(
        Student.id.label("student_id"), 
        Student.name.label("student_name"),
        Student.email.label("student_email"),
        func.sum(QuizAttempt.score).label("total_score")
    ).join(
        Student.quiz_attempts
    ).group_by(
        Student.id,
        Student.name,
        Student.email
    ).all()
