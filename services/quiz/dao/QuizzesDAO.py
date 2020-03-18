from models import db, Quiz

def quizCreate(quiz):
    db.session.add(quiz)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def quizRead(id):
    return Quiz.query.filter_by(id=id).first()

def quizUpdate():
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def quizDelete(id):
    quiz = quizRead(id)
    db.session.delete(quiz)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False