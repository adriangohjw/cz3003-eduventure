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

def validate_quiz_id(quiz_id):
    # if no 'quiz_id' found in params
    if (quiz_id is None):
        raise TypeError("Request params (quiz_id) not found")

    # if quiz_id params is empty
    if not quiz_id: 
        raise ValueError("quiz_id is empty")

    # check if type is integer
    if not isinstance(quiz_id, int):
        raise TypeError("quiz_id is not an integer")

def validate_score(score):
    # if no 'score' found in params
    if (score is None):
        raise TypeError("Request params (score) not found")

    # if score params is empty
    if not score: 
        raise ValueError("score is empty")

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
