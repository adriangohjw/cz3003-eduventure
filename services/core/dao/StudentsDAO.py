from models import db, Student, Rs_student_course_enrol

def studentCreate(student):
    db.session.add(student)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def studentRead(col, value):
    if (col == 'email'):
        return Student.query.filter_by(email=value).first()
    elif (col == 'id'):
        return Student.query.filter_by(id=value).first()
    else:
        return False

def studentUpdate():
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def courseMngCreate(rs):
    db.session.add(rs)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def courseMngRead(student_id, course_index):
    rs = Rs_student_course_enrol.query.filter_by(student_id=student_id).filter_by(course_index=course_index).first()
    return rs