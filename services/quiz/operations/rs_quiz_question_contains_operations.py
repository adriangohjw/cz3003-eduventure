from models import Rs_quiz_question_contain

from ..dao.QuestionsDAO import questionRead
from ..dao.QuizzesDAO import quizRead
from ..dao.RsQuizQuestionContainDAO import \
    rsQuizQuestionContainRead, rsQuizQuestionContainCreate, rsQuizQuestionContainDelete
from exceptions import ErrorWithCode

def initializeRsQuizQuestionContain(quiz_id, question_id):
    return Rs_quiz_question_contain(
        quiz_id = quiz_id,
        question_id = question_id
    )

def questionMngReadOperation(quiz_id):
    quiz = quizRead(quiz_id)

    # quiz is not found
    if quiz is None:
        raise ErrorWithCode(404, "No quiz found")

    # success case
    return quiz

def questionMngCreateOperation(quiz_id, question_id):
    quiz = quizRead(quiz_id)
    question = questionRead(question_id)

    # quiz is not found
    if quiz is None:
        raise ErrorWithCode(404, "No quiz found")

    # question is not found
    if question is None:
        raise ErrorWithCode(404, "No question found")

    rs = rsQuizQuestionContainRead(quiz.id, question.id)

    # if rs exist
    if rs is not None:
        raise ErrorWithCode(412, "Existing rs")

    rs = initializeRsQuizQuestionContain(quiz.id, question.id)
    if rsQuizQuestionContainCreate(rs) == False:
        raise ErrorWithCode(400, "Unsuccessful")

    # success case
    return rs

def questionMngDeleteOperation(quiz_id, question_id):
    quiz = quizRead(quiz_id)
    question = questionRead(question_id)

    # quiz is not found
    if quiz is None:
        raise ErrorWithCode(404, "No quiz found")

    # question is not found
    if question is None:
        raise ErrorWithCode(404, "No question found")

    rs = rsQuizQuestionContainRead(quiz.id, question.id)

    # if rs does not exist
    if rs is None:
        raise ErrorWithCode(412, "No rs found")

    if rsQuizQuestionContainDelete(quiz.id, question.id) == False:
        raise ErrorWithCode(400, "Unsuccessful")

    # success case
    return True
