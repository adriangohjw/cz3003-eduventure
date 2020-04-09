from exceptions import ErrorWithCode

from models import Rs_lesson_quiz_contain
from services.core.dao.RsLessonQuizContainDAO import \
    rsLessonQuizContainCreate, rsLessonQuizContainRead, rsLessonQuizContainDelete


def initializeRsLessonQuizContain(topic_id, lesson_id, quiz_id):
    return Rs_lesson_quiz_contain(topic_id, lesson_id, quiz_id)


def quizMngReadOperation(topic_id, lesson_id):
    
    rs = rsLessonQuizContainRead(topic_id, lesson_id)

    # rs is not found
    if len(rs) == 0:
        raise ErrorWithCode(404, "No rs found")

    # success case
    return rs


def quizMngCreateOperation(topic_id, lesson_id, quiz_id):

    rs = initializeRsLessonQuizContain(topic_id, lesson_id, quiz_id)
    if rsLessonQuizContainCreate(rs) == False:
        raise ErrorWithCode(400, "Unsuccessful")

    # success case
    return rs
    

def quizMngDeleteOperation(id):

    rs = Rs_lesson_quiz_contain.query.filter_by(id=id).first()

    if rs is None:
        raise ErrorWithCode(404, "No rs found")

    if rsLessonQuizContainDelete(id) == False:
        raise ErrorWithCode(400, "Unsuccessful")

    # success case
    return True
