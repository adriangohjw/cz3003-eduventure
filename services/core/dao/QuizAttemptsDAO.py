from models import db, QuizAttempt

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
