from models import db, QuestionChoice
from sqlalchemy import desc 

def questionChoiceCreate(questionChoice):
    db.session.add(questionChoice)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def questionChoiceRead(question_id, id):
    return QuestionChoice.query.filter_by(question_id=question_id).filter_by(id=id).first()

def questionChoiceUpdate():
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def questionChoiceDelete(question_id, id):
    questionChoice = questionChoiceRead(question_id, id)
    db.session.delete(questionChoice)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def getLastQuestionChoiceID(question_id):
    last_questionChoice = QuestionChoice.query.filter_by(question_id=question_id).order_by(desc(QuestionChoice.created_at)).first()
    if (last_questionChoice):
        return last_questionChoice.id 
    else:  
        return 0
