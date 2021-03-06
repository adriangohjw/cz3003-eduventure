from flask import request
from flask_restful import inputs

from services.quiz.contracts.quizzes_contracts import validate_id as validate_quiz_id


def validate_student_id(student_id):
    # if no 'student_id' found in params
    if (student_id is None):
        raise TypeError("Request params (student_id) not found")

    # check if student_id is a boolean
    # to check if bool before int because isinstance(student_id, int) returns True if student_id is bool
    if isinstance(student_id, bool):
        raise TypeError("student_id is not an integer")

    # check if type is integer
    if not isinstance(student_id, int):
        raise TypeError("student_id is not an integer")


def validate_winner_id(from_student_id, to_student_id, winner_id):
    # if no 'winner_id' found in params
    if (winner_id is None):
        raise TypeError("Request params (winner_id) not found")

    # check if winner_id is a boolean
    # to check if bool before int because isinstance(winner_id, int) returns True if winner_id is bool
    if isinstance(winner_id, bool):
        raise TypeError("winner_id is not an integer")

    # check if type is integer
    if not isinstance(winner_id, int):
        raise TypeError("winner_id is not an integer")

    # check if winner_id in (from_student_id, to_student_id)
    if (winner_id != from_student_id) and (winner_id != to_student_id):
        raise ValueError('winner_id not equal to from_student_id / to_student_id')


def validate_is_completed(is_completed):
    # if no 'is_completed' found in params
    if (is_completed is None):
        raise TypeError("Request params is_completed is not found")

    # check if type is boolean
    if not isinstance(is_completed, bool):
        raise TypeError("is_completed is not an boolean")


def challengeReadContract(request):
    from_student_id = request.args.get('from_student_id', type=int)
    to_student_id = request.args.get('to_student_id', type=int)
    quiz_id = request.args.get('quiz_id', type=int)
    is_completed = request.args.get('is_completed', type=inputs.boolean)

    if (from_student_id is None) and (to_student_id is None) and (quiz_id is None) and (is_completed is None):
        raise TypeError("no params being passed in")

    if (from_student_id is not None):
        validate_student_id(from_student_id)

    if (to_student_id is not None):
        validate_student_id(to_student_id)

    if (quiz_id is not None):
        validate_quiz_id(quiz_id)

    if (is_completed is not None):
        validate_is_completed(is_completed)

    return {
        'from_student_id': from_student_id,
        'to_student_id': to_student_id,
        'quiz_id': quiz_id,
        'is_completed': is_completed
    }


def challengeCreateContract(request):
    from_student_id = request.args.get('from_student_id', type=int)
    to_student_id = request.args.get('to_student_id', type=int)

    validate_student_id(from_student_id)
    validate_student_id(to_student_id)

    return {
        'from_student_id': from_student_id,
        'to_student_id': to_student_id
    }


def challengeUpdateCompletedContract(request):
    from_student_id = request.args.get('from_student_id', type=int)
    to_student_id = request.args.get('to_student_id', type=int)
    quiz_id = request.args.get('quiz_id', type=int)
    winner_id = request.args.get('winner_id', type=int)

    validate_student_id(from_student_id)
    validate_student_id(to_student_id)
    validate_quiz_id(quiz_id)

    if winner_id is not None:
        validate_winner_id(from_student_id, to_student_id, winner_id)

    return {
        'from_student_id': from_student_id,
        'to_student_id': to_student_id,
        'quiz_id': quiz_id,
        'winner_id': winner_id
    }
