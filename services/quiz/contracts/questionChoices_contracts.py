from flask import request

from services.quiz.contracts.questions_contracts import validate_id as validate_question_id

def validate_questionChoice_id(questionChoice_id):
    # if no 'questionChoice_id' found in params
    if (questionChoice_id is None):
        raise TypeError("Request params (questionChoice_id) not found")

    # if 'questionChoice_id' params is empty
    if not questionChoice_id: 
        raise ValueError("questionChoice_id is empty")

    # check if type is integer
    if not isinstance(questionChoice_id, int):
        raise TypeError("questionChoice_id is not an integer")

def validate_description(description):
    # if no 'description' found in params
    if (description is None):
        raise TypeError("Request params (description) not found")

    # if field params is empty
    if not description: 
        raise ValueError("description is empty")

def validate_is_correct(is_correct):
    # if no 'is_correct' found in params
    if (is_correct is None):
        raise TypeError("Request params is_correct is not found")

    # if is_correct params is empty
    if not is_correct:
        raise ValueError("is_correct is empty")

    # check if type is boolean
    if not isinstance(is_correct, bool):
        raise TypeError("is_correct is not an boolean")

def questionChoiceReadContract(request):  
    question_id = request.args.get('question_id', type=int)  
    questionChoice_id = request.args.get('questionChoice_id', type=int)

    validate_question_id(question_id)
    validate_questionChoice_id(questionChoice_id)

    return {
        'question_id': question_id,
        'questionChoice_id': questionChoice_id,
    }

def questionChoiceCreateContract(request):
    question_id = request.args.get('question_id', type=int)  
    description = request.args.get('description')
    is_correct = request.args.get('is_correct', type=bool)
    
    validate_question_id(question_id)
    validate_description(description)
    validate_is_correct(is_correct)
    
    return {
        'question_id': question_id,
        'description': description,
        'is_correct': is_correct
    }

def questionChoiceUpdateContract(request):
    question_id = request.args.get('question_id', type=int)  
    questionChoice_id = request.args.get('questionChoice_id', type=int)
    description = request.args.get('description')
    is_correct = request.args.get('is_correct', type=bool)

    validate_question_id(question_id)
    validate_questionChoice_id(questionChoice_id)

    if (description is None) and (is_correct is None):
        raise TypeError("no params being passed in")

    if (description is not None):
        validate_description(description)

    if (is_correct is not None):
        validate_is_correct(is_correct)
    
    return {
        'question_id': question_id,
        'questionChoice_id': questionChoice_id,
        'description': description,
        'is_correct': is_correct
    }

def questionChoiceDeleteContract(request):
    question_id = request.args.get('question_id', type=int)  
    questionChoice_id = request.args.get('questionChoice_id', type=int)

    validate_question_id(question_id)
    validate_questionChoice_id(questionChoice_id)

    return {
        'question_id': question_id,
        'questionChoice_id': questionChoice_id,
    }