from flask import request

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


def progressReadContract(student_id):
    student_id = request.args.get('student_id', type=int)

    validate_student_id(student_id)

    return {
        'student_id': student_id
    }
    