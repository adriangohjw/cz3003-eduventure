from models import QuestionAttempt

from ..dao.QuestionAttemptsDAO import \
    questionAttemptListRead, questionAttemptCreate

from ..dao.StudentsDAO import studentRead
from ...quiz.dao.QuestionsDAO import questionRead

from exceptions import ErrorWithCode

def initializeQuestionAttempt(student_id, question_id, is_correct, duration_ms):
    return QuestionAttempt(
        student_id=student_id, 
        question_id=question_id, 
        is_correct=is_correct, 
        duration_ms=int(duration_ms)
    )

def questionAttemptListReadOperation(student_id, question_id):
    student = studentRead(col='id', value=student_id)

    # student is not found
    if student is None:
        raise ErrorWithCode(409, "No student found")

    question = questionRead(question_id)

    # question is not found
    if question is None:
        raise ErrorWithCode(409, "No question found")

    questionAttemptList = questionAttemptListRead(student_id, question_id)

    # questionAttempt is not found
    if len(questionAttemptList) == 0:
        raise ErrorWithCode(409, "No questionAttempt found")

    # success case
    return questionAttemptList

def questionAttemptCreateOperation(student_id, question_id, is_correct, duration_ms):

    student = studentRead(col='id', value=student_id)

    # student is not found
    if student is None:
        raise ErrorWithCode(409, "No student found")

    question = questionRead(question_id)

    # question is not found
    if question is None:
        raise ErrorWithCode(409, "No question found")

    questionAttempt = initializeQuestionAttempt(student_id, question_id, is_correct, duration_ms)
    if questionAttemptCreate(questionAttempt) == False:
        raise ErrorWithCode(503, "Unsuccessful")

    # success case
    return questionAttempt
