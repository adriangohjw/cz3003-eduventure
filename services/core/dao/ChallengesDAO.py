from models import db, Challenge

def challengeCreate(challenge):
    db.session.add(challenge)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False


def challengeRead(from_student_id, to_student_id, quiz_id, is_completed):
    
    challenges = Challenge.query

    if (from_student_id is not None):
        challenges = challenges.filter_by(from_student_id=from_student_id)

    if (to_student_id is not None):
        challenges = challenges.filter_by(to_student_id=to_student_id)

    if (quiz_id is not None):
        challenges = challenges.filter_by(quiz_id=quiz_id)

    if (is_completed is not None):
        challenges = challenges.filter_by(is_completed=is_completed)

    return challenges.all()


def challengeUpdate():
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False
