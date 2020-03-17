from models import db, Student

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
