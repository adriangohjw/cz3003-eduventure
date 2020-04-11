from flask import request

from services.core.contracts.courses_contracts import validate_index as validate_course_index


def studentScoreReadContract(student_id):
    student_id = request.args.get('student_id', type=int)

    return {
        'student_id': student_id
    }
