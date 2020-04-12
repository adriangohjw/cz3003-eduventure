from flask import request

import datetime
from dateutil.parser import parse

from services.quiz.contracts.quizzes_contracts import \
    validate_date_start, validate_date_end


def validate_id(id):
    # if no 'id' found in params
    if (id is None):
        raise TypeError("Request params (id) not found")

    # if id params is empty
    if not id: 
        raise ValueError("id is empty")

    # check if type is integer
    if not isinstance(id, int):
        raise TypeError("id is not an integer")


def leaderboardReadContract(request):
    student_id = request.args.get('student_id', type=int)

    return {
        'student_id': student_id
    }


def studentScoreReadContract(request):
    student_id = request.args.get('student_id', type=int)

    return {
        'student_id': student_id
    }


def courseScoreReadContract(request):
    course_index = request.args.get('course_index')

    return {
        'course_index': course_index
    }


def activityReadContract(request):
    date_start = request.args.get('date_start')
    date_end = request.args.get('date_end')
    student_id = request.args.get('student_id', type=int)

    validate_date_start(date_start)
    validate_date_end(date_end)
    validate_id(student_id)

    return {
        'date_start': datetime.date(parse(date_start).year, parse(date_start).month, parse(date_start).day),
        'date_end': datetime.date(parse(date_end).year, parse(date_end).month, parse(date_end).day),
        'student_id': student_id
    }
