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

def questionAttemptListRead(student_id, question_id=None):

    if question_id is None:
        return QuestionAttempt.query.filter_by(student_id=student_id).all()
    
    return QuestionAttempt.query.\
        filter_by(student_id=student_id).filter_by(question_id=question_id).all()
            