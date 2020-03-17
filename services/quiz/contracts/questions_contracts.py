from flask import request

def validate_id(id, type):
    # if no 'id'/'topic_id'/'lesson_id' found in params
    if (id is None):
        raise Exception("Request params ({}}) not found".format(type))

    # if 'id'/'topic_id'/'lesson_id' params is empty
    if not id: 
        raise Exception("{}} is empty".format(type))

def validate_description(description):
    # if no 'description' found in params
    if (description is None):
        raise Exception("Request params (description) not found")

    # if description params is empty
    if not description: 
        raise Exception("Description is empty")

def questionReadContract(request):    
    id = request.args.get('id')

    validate_id(id, 'id')

    return {
        'id': id
    }

def questionCreateContract(request):
    topic_id = request.args.get('topic_id')
    lesson_id = request.args.get('lesson_id')
    description = request.args.get('description')
    
    validate_id(topic_id, 'topic_id')
    validate_id(lesson_id, 'lesson_id')
    validate_description(description)
    
    return {
        'topic_id': topic_id,
        'lesson_id': lesson_id,
        'description': description
    }

def questionUpdateContract(request):
    id = request.args.get('id')
    description = request.args.get('description')

    validate_id(id, 'id')
    validate_description(description)
    
    return {
        'id': id,
        'description': description
    }

def questionDeleteContract(request):
    id = request.args.get('id')

    validate_id(id, 'id')

    return {
        'id': id
    }