from exceptions import ErrorWithCode

from models import Rs_lesson_quiz_contain, Topic, Lesson
from services.core.dao.RsLessonQuizContainDAO import \
    rsLessonQuizContainCreate, rsLessonQuizContainRead, rsLessonQuizContainDelete


def initializeRsLessonQuizContain(topic_id, lesson_id, quiz_id):
    return Rs_lesson_quiz_contain(topic_id, lesson_id, quiz_id)


def quizMngReadOperation(topic_id, lesson_id):
    
    rs = rsLessonQuizContainRead(topic_id, lesson_id)

    # rs is not found
    if len(rs) == 0:
        raise ErrorWithCode(409, "No rs found")

    # success case
    return rs


def quizMngCreateOperation(topic_id, lesson_id, quiz_id):

    # dependency not found
    topic = Topic.query.filter_by(id=topic_id).first()
    if topic is None:
        raise ErrorWithCode(409, "topic not found")

    # dependency not found
    lesson = Lesson.query.filter_by(topic_id=topic_id).filter_by(id=lesson_id).first()
    if lesson is None:
        raise ErrorWithCode(409, "lesson not found")

    # existing rs found
    rs = Rs_lesson_quiz_contain.query.filter_by(topic_id=topic_id).filter_by(lesson_id=lesson_id).filter_by(quiz_id=quiz_id).first() 
    if rs is not None:
        raise ErrorWithCode(409, "existing relationship found")

    rs = initializeRsLessonQuizContain(topic_id, lesson_id, quiz_id)
    if rsLessonQuizContainCreate(rs) == False:
        raise ErrorWithCode(503, "Unsuccessful")

    # success case
    return rs
    

def quizMngDeleteOperation(id):

    rs = Rs_lesson_quiz_contain.query.filter_by(id=id).first()

    if rs is None:
        raise ErrorWithCode(409, "No rs found")

    if rsLessonQuizContainDelete(id) == False:
        raise ErrorWithCode(503, "Unsuccessful")

    # success case
    return True
