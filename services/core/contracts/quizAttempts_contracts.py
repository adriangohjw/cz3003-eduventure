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

def validate_quiz_id(quiz_id):
    # if no 'quiz_id' found in params
    if (quiz_id is None):
        raise TypeError("Request params (quiz_id) not found")

    # check if quiz_id is a boolean
    # to check if bool before int because isinstance(quiz_id, int) returns True if quiz_id is bool
    if isinstance(quiz_id, bool):
        raise TypeError("quiz_id is not an integer")

    # check if type is integer
    if not isinstance(quiz_id, int):
        raise TypeError("quiz_id is not an integer")

def validate_score(score):
    # if no 'score' found in params
    if (score is None):
        raise TypeError("Request params (score) not found")

    # check if score is a boolean
    # to check if bool before int because isinstance(score, int) returns True if score is bool
    if isinstance(score, bool):
        raise TypeError("score is not an integer")

    # check if type is integer
    if not isinstance(score, int):
        raise TypeError("score is not an integer")

    # ensure score is less than 0
    if int(score) < 0:
        raise ValueError("score must be more than or equal to zero")

def quizAttemptListReadContract(request):    
    student_id = request.args.get('student_id', type=int)
    quiz_id = request.args.get('quiz_id', type=int)

    validate_student_id(student_id)
    validate_quiz_id(quiz_id)

    return {
        'student_id': student_id,
        'quiz_id': quiz_id
    }

def quizAttemptCreateContract(request):
    student_id = request.args.get('student_id', type=int)
    quiz_id = request.args.get('quiz_id', type=int)
    score = request.args.get('score', type=int)

    validate_student_id(student_id)
    validate_quiz_id(quiz_id)
    validate_score(score)

    return {
        'student_id': student_id,
        'quiz_id': quiz_id,
        'score': score
    }
