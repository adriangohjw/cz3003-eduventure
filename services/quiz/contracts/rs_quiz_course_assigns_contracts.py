from flask import request

from .quizzes_contracts import validate_id
from ...core.contracts.courses_contracts import validate_index

def courseMngReadContract(request):    
    quiz_id = request.args.get('quiz_id')

    validate_id(quiz_id)

    return {
        'quiz_id': quiz_id
    }

def courseMngCreateContract(request):
    quiz_id = request.args.get('quiz_id')
    course_index = request.args.get('course_index')

    validate_id(quiz_id)
    validate_index(course_index)

    return {
        'quiz_id': quiz_id,
        'course_index': course_index
    }
