from models import db, QuestionAttempt, Student
from sqlalchemy import func

def questionAttemptCreate(questionAttempt):
    db.session.add(questionAttempt)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def questionAttemptListRead(student_id, question_id):
    return QuestionAttempt.query.\
        filter_by(student_id=student_id).filter_by(question_id=question_id).all()
            
def questionAttemptLeaderboardRead():
    return db.session.query(
        Student.id.label("student_id"), 
        Student.name.label("student_name"),
        Student.email.label("student_email"),
        func.count(QuestionAttempt.is_correct).label("total_score")
    ).join(
        Student.questions_attempts
    ).filter_by(
        is_correct = True
    ).group_by(
        Student.id,
        Student.name,
        Student.email
    ).all()
