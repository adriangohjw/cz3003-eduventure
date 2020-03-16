from models import db, Staff, Rs_staff_course_teach

def staffCreate(staff):
    db.session.add(staff)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def staffRead(col, value):
    if (col == 'email'):
        return Staff.query.filter_by(email=value).first()
    elif (col == 'id'):
        return Staff.query.filter_by(id=value).first()
    else:
        return False

def staffUpdate():
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

def courseMngRead(staff_id, course_index):
    rs = Rs_staff_course_teach.query.filter_by(staff_id=staff_id).filter_by(course_index=course_index).first()
    return rs