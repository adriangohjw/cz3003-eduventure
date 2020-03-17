from flask import request

def validate_id(id, type):
    # if no 'id' found in params
    if (id is None):
        raise Exception("Request params ({}) not found".format(type))

    # if 'id' params is empty
    if not id: 
        raise Exception("{}} is empty".format(type))

def validate_description(description):
    # if no 'description' found in params
    if (description is None):
        raise Exception("Request params (description) not found")

    # if field params is empty
    if not description: 
        raise Exception("description is empty")

def validate_col(col):
    # if no 'col' found in params
    if (col is None):
        raise Exception("Request params (col) not found")

    # if field params is empty
    if not col: 
        raise Exception("col is empty")

    if col not in ('description', 'is_correct'):
        raise Exception("Invalid request in params (col)")

def validate_is_correct(is_correct):
    # if no 'is_correct' found in params
    if (is_correct is None):
        raise Exception("Request params is_correct is not found")

    # if is_correct params is empty
    if not is_correct:
        raise Exception("is_correct is empty")

    if is_correct not in ('True', 'False'):
        raise Exception("is_correct is not boolean")

def questionChoiceReadContract(request):  
    question_id = request.args.get('question_id')  
    questionChoice_id = request.args.get('questionChoice_id')

    validate_id(question_id, 'question_id')
    validate_id(questionChoice_id, 'questionChoice_id')

    return {
        'question_id': question_id,
        'questionChoice_id': questionChoice_id,
    }

def questionChoiceCreateContract(request):
    question_id = request.args.get('question_id')  
    description = request.args.get('description')
    is_correct = request.args.get('is_correct')
    
    validate_id(question_id, 'question_id')
    validate_description(description, 'description')
    validate_is_correct(is_correct)

    is_correct = True if is_correct == 'True' else False
    
    return {
        'question_id': question_id,
        'description': description,
        'is_correct': is_correct
    }

def questionChoiceUpdateContract(request):
    question_id = request.args.get('question_id')  
    questionChoice_id = request.args.get('questionChoice_id')
    col = request.args.get('col')
    value = request.args.get('value')

    validate_id(question_id, 'question_id')
    validate_id(questionChoice_id, 'questionChoice_id')
    validate_col(col)

    if col == 'description':
        validate_description(value)
    elif col == 'is_correct':
        validate_is_correct(value)
        value = True if value == 'True' else False
    
    return {
        'question_id': question_id,
        'questionChoice_id': questionChoice_id,
        'col': col,
        'value': value
    }

def questionChoiceDeleteContract(request):
    question_id = request.args.get('question_id')  
    questionChoice_id = request.args.get('questionChoice_id')

    validate_id(question_id, 'question_id')
    validate_id(questionChoice_id, 'questionChoice_id')

    return {
        'question_id': question_id,
        'questionChoice_id': questionChoice_id,
    }