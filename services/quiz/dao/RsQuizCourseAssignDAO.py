from models import db, Rs_quiz_course_assign

def rsQuizCourseAssignCreate(rs):
    db.session.add(rs)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def rsQuizCourseAssignRead(quiz_id, course_index):
    return Rs_quiz_course_assign.query.\
        filter_by(quiz_id=quiz_id).filter_by(course_index=course_index).first()
