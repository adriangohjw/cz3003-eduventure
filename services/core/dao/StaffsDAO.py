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
        