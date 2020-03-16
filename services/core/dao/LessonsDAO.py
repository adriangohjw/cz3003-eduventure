from models import db, Lesson

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