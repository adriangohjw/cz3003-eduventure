from models import db, Rs_lesson_quiz_contain

def rsLessonQuizContainCreate(rs):
    db.session.add(rs)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def rsLessonQuizContainRead(topic_id, lesson_id):
    return Rs_lesson_quiz_contain.query.filter_by(topic_id=topic_id).filter_by(lesson_id=lesson_id).all()

def rsLessonQuizContainDelete(id):
    rs = Rs_lesson_quiz_contain.query.filter_by(id=id).first()
    db.session.delete(rs)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False
