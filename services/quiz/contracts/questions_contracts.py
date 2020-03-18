from flask import request

def validate_id(id):
    # if no 'id' found in params
    if (id is None):
        raise Exception("Request params (id) not found")

    # if 'id' params is empty
    if not id: 
        raise Exception("id is empty")

def validate_topic_id(topic_id):
    # if no 'topic_id' found in params
    if (topic_id is None):
        raise Exception("Request params (topic_id) not found")

    # if 'topic_id' params is empty
    if not topic_id: 
        raise Exception("topic_id is empty")   

def validate_lesson_id(lesson_id):
    # if no 'lesson_id' found in params
    if (lesson_id is None):
        raise Exception("Request params (lesson_id) not found")

    # if 'lesson_id' params is empty
    if not lesson_id: 
        raise Exception("lesson_id is empty")   

def validate_description(description):
    # if no 'description' found in params
    if (description is None):
        raise Exception("Request params (description) not found")

    # if description params is empty
    if not description: 
        raise Exception("Description is empty")

def questionReadContract(request):    
    id = request.args.get('id')

    validate_id(id)

    return {
        'id': id
    }

def questionCreateContract(request):
    topic_id = request.args.get('topic_id')
    lesson_id = request.args.get('lesson_id')
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
    id = request.args.get('id')
    description = request.args.get('description')

    validate_id(id)
    validate_description(description)
    
    return {
        'id': id,
        'description': description
    }

def questionDeleteContract(request):
    id = request.args.get('id')

    validate_id(id)

    return {
        'id': id
    }