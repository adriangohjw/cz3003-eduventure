from flask import request
from flask_restful import inputs

def validate_student_id(student_id):
    # if no 'student_id' found in params
    if (student_id is None):
        raise TypeError("Request params (student_id) not found")

    # if student_id params is empty
    if not student_id: 
        raise ValueError("student_id is empty")

    # check if type is integer
    if not isinstance(student_id, int):
        raise TypeError("student_id is not an integer")

def validate_question_id(question_id):
    # if no 'question_id' found in params
    if (question_id is None):
        raise TypeError("Request params (question_id) not found")

    # if question_id params is empty
    if not question_id: 
        raise ValueError("question_id is empty")

    # check if type is integer
    if not isinstance(question_id, int):
        raise TypeError("question_id is not an integer")

def validate_duration_ms(duration_ms):
    # if no 'duration_ms' found in params
    if (duration_ms is None):
        raise TypeError("Request params (duration_ms) not found")

    # if duration params is empty
    if not duration_ms: 
        raise ValueError("duration_ms is empty")

    # check if duration is integer
    if not isinstance(duration_ms, int):
        raise TypeError("duration_ms needs to be integer")

    # ensure duration is more than 0
    if int(duration_ms) <= 0:
        raise ValueError("duration_ms must be more than zero")

def validate_is_correct(is_correct):
    # if no 'is_correct' found in params
    if (is_correct is None):
        raise TypeError("Request params is_correct is not found")

    # check if type is boolean
    if not isinstance(is_correct, bool):
        raise TypeError("is_correct is not an boolean")

def questionAttemptListReadContract(request):    
    student_id = request.args.get('student_id', type=int)
    question_id = request.args.get('question_id', type=int)

    validate_student_id(student_id)
    validate_question_id(question_id)

    return {
        'student_id': int(student_id),
        'question_id': int(question_id),
    }

def questionAttemptCreateContract(request):
    student_id = request.args.get('student_id', type=int)
    question_id = request.args.get('question_id', type=int)
    is_correct = request.args.get('is_correct', type=inputs.boolean)
    duration_ms = request.args.get('duration_ms', type=int)

    validate_student_id(student_id)
    validate_question_id(question_id)
    validate_is_correct(is_correct)
    validate_duration_ms(duration_ms)

    return {
        'student_id': int(student_id),
        'question_id': int(question_id),
        'is_correct': bool(is_correct),
        'duration_ms': int(duration_ms)
    }
