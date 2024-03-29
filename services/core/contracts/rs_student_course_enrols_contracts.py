from flask import request

from .users_contracts import validate_email
from .courses_contracts import validate_index

def courseMngReadContract(request):    
    user_email = request.args.get('user_email')

    validate_email(user_email)

    return {
        'user_email': user_email
    }

def courseMngCreateContract(request):
    user_email = request.args.get('user_email')
    course_index = request.args.get('course_index')

    validate_email(user_email)
    validate_index(course_index)

    return {
        'user_email': user_email,
        'course_index': course_index
    }

def courseClasslistReadContract(request):
    course_index = request.args.get('course_index')

    if course_index is not None:
        validate_index(course_index)

    return {
        'course_index': course_index
    }
