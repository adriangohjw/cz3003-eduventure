from models import db, Rs_quiz_question_contain

def rsQuizQuestionContainCreate(rs):
    db.session.add(rs)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def rsQuizQuestionContainRead(quiz_id, question_id):
    return Rs_quiz_question_contain.query.\
        filter_by(quiz_id=quiz_id).filter_by(question_id=question_id).first()

def rsQuizQuestionContainDelete(quiz_id, question_id):
    rs = rsQuizQuestionContainRead(quiz_id, question_id)
    db.session.delete(rs)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False
