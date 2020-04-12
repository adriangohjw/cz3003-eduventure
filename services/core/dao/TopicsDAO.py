from models import db, Topic

def topicCreate(topic):
    db.session.add(topic)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def topicRead(col, value):
    if (col == 'name'):
        return Topic.query.filter_by(name=value).first()
    elif (col == 'id'):
        return Topic.query.filter_by(id=value).first()
    else:
        return False

def topicUpdate():
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def topiclistRead():
    return Topic.query.all()
    