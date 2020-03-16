from models import db, User

def userCreate(user):
    db.session.add(user)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def userRead(col, value):
    if (col == 'email'):
        return User.query.filter_by(email=value).first()
    elif (col == 'id'):
        return User.query.filter_by(id=value).first()
    else:
        return False

def userUpdate():
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False