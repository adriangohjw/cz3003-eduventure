from models import db, Question

def questionCreate(question):
    db.session.add(question)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def questionRead(id):
    return Question.query.filter_by(id=id).first()

def questionUpdate():
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False