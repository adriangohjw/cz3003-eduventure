from models import db, Lesson
from sqlalchemy import desc 

def lessonCreate(lesson):
    db.session.add(lesson)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def lessonRead(topic_id, col, value):
    if (col == 'name'):
        return Lesson.query.filter_by(topic_id=topic_id).filter_by(name=value).first()
    elif (col == 'id'):
        return Lesson.query.filter_by(topic_id=topic_id).filter_by(id=value).first()
    else:
        return False

def lessonUpdate():
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def lessonDelete(topic_id, lesson_id):
    lesson = lessonRead(topic_id=topic_id, col='id', value=lesson_id)
    db.session.delete(lesson)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def getLastLessonID(topic_id):
    return Lesson.query.filter_by(topic_id=topic_id).order_by(desc(Lesson.created_at)).first().id