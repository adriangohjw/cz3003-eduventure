from models import db, Rs_staff_course_teach

def rsStaffCourseTeachCreate(rs):
    db.session.add(rs)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def rsStaffCourseTeachRead(staff_id, course_index):
    return Rs_staff_course_teach.query.filter_by(staff_id=staff_id).filter_by(course_index=course_index).first()
