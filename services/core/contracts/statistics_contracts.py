from flask import request

def studentScoreReadContract(student_id):
    student_id = request.args.get('student_id', type=int)

    return {
        'student_id': student_id
    }


def courseScoreReadContract(course_index):
    course_index = request.args.get('course_index')

    return {
        'course_index': course_index
    }
