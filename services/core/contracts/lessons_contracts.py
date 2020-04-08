from flask import request

def validate_topic_id(topic_id):
    # if no 'topic_id' found in params
    if (topic_id is None):
        raise TypeError("Request params (topic_id) not found")

    # if topic_id params is empty
    if not topic_id: 
        raise ValueError("Topic_id is empty")

    # check if type is integer
    if not isinstance(topic_id, int):
        raise TypeError("topic_id is not an integer")

def validate_lesson_id(lesson_id):
    # if no 'lesson_id' found in params
    if (lesson_id is None):
        raise TypeError("Request params (lesson_id) not found")

    # if lesson_id params is empty
    if not lesson_id: 
        raise ValueError("Lesson_id is empty")

    # check if type is integer
    if not isinstance(lesson_id, int):
        raise TypeError("lesson_id is not an integer")

def validate_name(name):
    # if no 'name' found in params
    if (name is None):
        raise TypeError("Request params (name) not found")

    # if name params is empty
    if not name: 
        raise ValueError("Name is empty")

def validate_content(content):
    # if no 'content' found in params
    if (content is None):
        raise TypeError("Request params (content) not found")

    # if content params is empty
    if not content: 
        raise ValueError("Content is empty")


def lessonReadContract(request):    
    topic_id = request.args.get('topic_id', type=int)
    lesson_id = request.args.get('lesson_id', type=int)

    validate_topic_id(topic_id)
    validate_lesson_id(lesson_id)

    return {
        'topic_id': topic_id,
        'lesson_id': lesson_id
    }

def lessonCreateContract(request):
    topic_id = request.args.get('topic_id', type=int)
    name = request.args.get('name')
    content = request.args.get('content')
    
    validate_topic_id(topic_id)
    validate_name(name)
    validate_content(content)
    
    return {
        'topic_id': topic_id,
        'name': name,
        'content': content
    }

def lessonUpdateContract(request):
    topic_id = request.args.get('topic_id', type=int)
    lesson_id = request.args.get('lesson_id', type=int)
    col = request.args.get('col')
    value = request.args.get('value')

    validate_topic_id(topic_id)
    validate_lesson_id(lesson_id)

    if (col == 'name'):
        validate_name(value)
    elif (col == 'content'):
        validate_content(value)
    else:
        raise Exception("Request params (name / content) not found")
    
    return {
        'topic_id': topic_id,
        'lesson_id': lesson_id,
        'col': col,
        'value': value      
    }

def lessonDeleteContract(request):
    topic_id = request.args.get('topic_id', type=int)
    lesson_id = request.args.get('lesson_id', type=int)

    validate_topic_id(topic_id)
    validate_lesson_id(lesson_id)

    return {
        'topic_id': topic_id,
        'lesson_id': lesson_id
    }
