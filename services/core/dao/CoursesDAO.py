from models import db, Course

def courseCreate(course):
    db.session.add(course)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def courseRead(index):
    return Course.query.filter_by(index=index).first()