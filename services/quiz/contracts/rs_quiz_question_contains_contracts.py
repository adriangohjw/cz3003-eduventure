from flask import request

from .quizzes_contracts import validate_id as validate_quiz_id
from .questions_contracts import validate_id as validate_question_id

def questionMngReadContract(request):    
    quiz_id = request.args.get('quiz_id', type=int)

    validate_quiz_id(quiz_id)

    return {
        'quiz_id': quiz_id
    }

def questionMngCreateContract(request):
    quiz_id = request.args.get('quiz_id', type=int)
    question_id = request.args.get('question_id', type=int)

    validate_quiz_id(quiz_id)
    validate_question_id(question_id)

    return {
        'quiz_id': quiz_id,
        'question_id': question_id
    }
