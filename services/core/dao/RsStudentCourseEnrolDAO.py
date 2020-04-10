from models import db, Rs_student_course_enrol

def rsStudentCourseEnrolCreate(rs):
    db.session.add(rs)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def rsStudentCourseEnrolRead(student_id, course_index):
    return Rs_student_course_enrol.query.filter_by(student_id=student_id).filter_by(course_index=course_index).first()

def rsCourseEnrolRead(course_index):
    return Rs_student_course_enrol.query.filter_by(course_index=course_index).all()
