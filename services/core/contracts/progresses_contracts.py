from flask import request

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


def progressReadContract(student_id):
    student_id = request.args.get('student_id', type=int)

    validate_student_id(student_id)

    return {
        'student_id': student_id
    }
    