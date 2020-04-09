from flask import request

from services.core.contracts.topics_contracts import validate_id as validate_topic_id
from services.core.contracts.lessons_contracts import validate_lesson_id

def validate_id(id):
    # if no 'id' found in params
    if (id is None):
        raise TypeError("Request params (id) not found")

    # if 'id' params is empty
    if not id: 
        raise ValueError("id is empty")

    # check if type is integer
    if not isinstance(id, int):
        raise TypeError("id is not an integer")

def validate_description(description):
    # if no 'description' found in params
    if (description is None):
        raise TypeError("Request params (description) not found")

    # if description params is empty
    if not description: 
        raise ValueError("Description is empty")

def questionReadContract(request):    
    id = request.args.get('id', type=int)

    validate_id(id)

    return {
        'id': id
    }

def questionCreateContract(request):
    topic_id = request.args.get('topic_id', type=int)
    lesson_id = request.args.get('lesson_id', type=int)
    description = request.args.get('description')
    
    validate_topic_id(topic_id)
    validate_lesson_id(lesson_id)
    validate_description(description)
    
    return {
        'topic_id': topic_id,
        'lesson_id': lesson_id,
        'description': description
    }

def questionUpdateContract(request):
    id = request.args.get('id', type=int)
    description = request.args.get('description')

    validate_id(id)
    validate_description(description)
    
    return {
        'id': id,
        'description': description
    }

def questionDeleteContract(request):
    id = request.args.get('id', type=int)

    validate_id(id)

    return {
        'id': id
    }