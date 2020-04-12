from exceptions import ErrorWithCode

from models import Challenge
from services.core.dao.ChallengesDAO import \
    challengeCreate, challengeRead, challengeUpdate


def initializeChallenge(from_student_id, to_student_id, quiz_id):
    return Challenge(from_student_id, to_student_id, quiz_id)


def challengeReadOperation(from_student_id, to_student_id, quiz_id, is_completed):

    challenges = challengeRead(from_student_id, to_student_id, quiz_id, is_completed)

    # challenge is not found
    if len(challenges) == 0:
        raise ErrorWithCode(404, "No challenge found")

    # success case
    return challenges


def challengeCreateOperation(from_student_id, to_student_id, quiz_id):

    challenge = challengeRead(from_student_id, to_student_id, quiz_id, None)

    # if challenge exist found
    if challenge:
        raise ErrorWithCode(412, "Existing challenge")

    challenge = initializeChallenge(from_student_id, to_student_id, quiz_id)
    if challengeCreate(challenge) == False:
        raise ErrorWithCode(400, "Unsuccessful")

    # success case
    return challenge


def challengeUpdateCompletedOperation(from_student_id, to_student_id, quiz_id, winner_id):

    challenges = challengeRead(from_student_id, to_student_id, quiz_id, None)

    # challenge is not found
    if len(challenges) == 0:
        raise ErrorWithCode(404, "No challenge found")

    challenge = challenges[0]

    challenge.is_completed = True
    challenge.winner_id = winner_id
    if challengeUpdate() == False:
        raise ErrorWithCode(400, "Unsuccessful")

    # success case
    return challenge
