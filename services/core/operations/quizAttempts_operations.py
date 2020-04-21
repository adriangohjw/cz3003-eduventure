from models import QuizAttempt

from ...core.dao.StudentsDAO import studentRead
from ...quiz.dao.QuizzesDAO import quizRead
from ..dao.QuizAttemptsDAO import quizAttemptListRead, quizAttemptCreate

from exceptions import ErrorWithCode

def initializeQuizAttempt(student_id, quiz_id, score):
    return QuizAttempt(
        student_id = student_id,
        quiz_id = quiz_id,
        score = int(score)
    )

def quizAttemptListReadOperation(student_id, quiz_id):
    student = studentRead(col='id', value=student_id)

    # student is not found
    if student is None:
        raise ErrorWithCode(409, "No student found")

    quiz = quizRead(quiz_id)

    # quiz is not found
    if quiz is None:
        raise ErrorWithCode(409, "No quiz found")

    quizAttemptList = quizAttemptListRead(student.id, quiz.id)

    # quizAttempt is not found
    if len(quizAttemptList) == 0:
        raise ErrorWithCode(409, "No quizAttempt found")

    # success case
    return quizAttemptList

def quizAttemptCreateOperation(student_id, quiz_id, score):

    student = studentRead(col='id', value=student_id)

    # student is not found
    if student is None:
        raise ErrorWithCode(409, "No student found")

    quiz = quizRead(quiz_id)

    # quiz is not found
    if quiz is None:
        raise ErrorWithCode(409, "No quiz found")

    quizAttempt = initializeQuizAttempt(student_id, quiz_id, score)
    if quizAttemptCreate(quizAttempt) == False:
        raise ErrorWithCode(503, "Unsuccessful")

    # success case
    return quizAttempt
