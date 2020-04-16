import secrets
from datetime import datetime, timedelta

from exceptions import ErrorWithCode

from models import Challenge

from services.core.dao.ChallengesDAO import \
    challengeCreate, challengeRead, challengeUpdate

from services.core.dao.StudentsDAO import \
    studentRead

from services.core.dao.QuestionAttemptsDAO import \
    questionAttemptListRead

from services.quiz.operations.quizzes_operations import \
    initializeQuiz

from services.quiz.dao.QuizzesDAO import \
    quizCreate 

from services.quiz.operations.rs_quiz_question_contains_operations import \
    initializeRsQuizQuestionContain

from services.quiz.dao.RsQuizQuestionContainDAO import \
    rsQuizQuestionContainCreate


def initializeChallenge(from_student_id, to_student_id, quiz_id):
    return Challenge(from_student_id, to_student_id, quiz_id)


def challengeReadOperation(from_student_id, to_student_id, quiz_id, is_completed):

    challenges = challengeRead(from_student_id, to_student_id, quiz_id, is_completed)

    # success case
    return challenges


def challengeCreateOperation(from_student_id, to_student_id):

    # check if students exists
    from_student = studentRead(col='id', value=from_student_id)
    to_student = studentRead(col='id', value=to_student_id)
    if (from_student is None) or (to_student is None):
        raise ErrorWithCode(409, "students do not exist")

    # find questions attempts by from_student
    from_student_question_attempts = questionAttemptListRead(from_student_id, None)
    from_student_question_attempts_id_list = [qa.question_id for qa in from_student_question_attempts]   

    # find questions attempts by to_student
    to_student_question_attempts = questionAttemptListRead(to_student_id, None)
    to_student_question_attempts_id_list = [qa.question_id for qa in to_student_question_attempts]

    # find common questions attempts by both students
    common_question_attempts_id_list = list(set(from_student_question_attempts_id_list).intersection(to_student_question_attempts_id_list))

    # if less than 3 common attempts
    if len(common_question_attempts_id_list) < 3:
        raise ErrorWithCode(409, "Less than 3 common questions attempted by both students")

    # pick 3 random questions from the list
    secure_random = secrets.SystemRandom()
    questions_in_challenge = secure_random.sample(common_question_attempts_id_list, 3)

    # create a new quiz
    # assuming challenge ends in 3 days
    new_quiz = initializeQuiz(
        staff_id=None, 
        name='challenge',
        is_fast=True,
        date_start=datetime.today().strftime('%Y-%m-%d'),
        date_end=(datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
    ) 
    if quizCreate(new_quiz) == False:
        raise ErrorWithCode(503, "Unsuccessful")

    # add questions to the quiz
    for question_id in questions_in_challenge:
        rs = initializeRsQuizQuestionContain(quiz_id=new_quiz.id, question_id=question_id)
        if rsQuizQuestionContainCreate(rs) == False:
            raise ErrorWithCode(503, "Unsuccessful")

    # create challenge
    challenge = initializeChallenge(from_student_id, to_student_id, new_quiz.id)
    if challengeCreate(challenge) == False:
        raise ErrorWithCode(503, "Unsuccessful")

    # success case
    return challenge


def challengeUpdateCompletedOperation(from_student_id, to_student_id, quiz_id, winner_id):

    challenges = challengeRead(from_student_id, to_student_id, quiz_id, None)

    # challenge is not found
    if len(challenges) == 0:
        raise ErrorWithCode(409, "No challenge found")

    challenge = challenges[0]

    challenge.is_completed = True
    challenge.winner_id = winner_id
    if challengeUpdate() == False:
        raise ErrorWithCode(503, "Unsuccessful")

    # success case
    return challenge
