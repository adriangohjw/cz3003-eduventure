from flask import request

from services.core.contracts.topics_contracts import validate_id as validate_topic_id
from services.core.contracts.lessons_contracts import validate_lesson_id
from services.quiz.contracts.quizzes_contracts import validate_id as validate_quiz_id


def validate_id(id):
    # if no 'id' found in params
    if (id is None):
        raise TypeError("Request params (id) not found")

    # check if id is a boolean
    # to check if bool before int because isinstance(id, int) returns True if id is bool
    if isinstance(id, bool):
        raise TypeError("Id is not an integer")

    # check if type is integer
    if not isinstance(id, int):
        raise TypeError("Id is not an integer")


def quizMngReadContract(request):

    topic_id = request.args.get('topic_id', type=int)
    lesson_id = request.args.get('lesson_id', type=int)

    validate_topic_id(topic_id)
    validate_lesson_id(lesson_id)

    return {
        'topic_id': topic_id,
        'lesson_id': lesson_id
    }


def quizMngCreateContract(request):

    topic_id = request.args.get('topic_id', type=int)
    lesson_id = request.args.get('lesson_id', type=int)
    quiz_id = request.args.get('quiz_id', type=int)

    validate_topic_id(topic_id)
    validate_lesson_id(lesson_id)
    validate_quiz_id(quiz_id)

    return {
        'topic_id': topic_id,
        'lesson_id': lesson_id,
        'quiz_id': quiz_id
    }


def quizMngDeleteContract(request):

    id = request.args.get('id', type=int)

    validate_id(id)

    return {
        'id': id,
    }
