from flask import request
import validators

from services.core.contracts.topics_contracts import validate_id as validate_topic_id


def validate_lesson_id(lesson_id):
    # if no 'lesson_id' found in params
    if (lesson_id is None):
        raise TypeError("Request params (lesson_id) not found")

    # check if lesson_id is a boolean
    # to check if bool before int because isinstance(lesson_id, int) returns True if lesson_id is bool
    if isinstance(lesson_id, bool):
        raise TypeError("lesson_id is not an integer")

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

def validate_url_link(url_link):
    # if url_link params is empty
    if not url_link: 
        raise ValueError("url_link is empty")

    # check if URL is valid
    if not validators.url(url_link):
        raise ValueError("url_link is not valid")

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
    url_link = request.args.get('url_link')
    
    validate_topic_id(topic_id)
    validate_name(name)
    validate_content(content)

    if url_link is not None:
        validate_url_link(url_link)
    
    return {
        'topic_id': topic_id,
        'name': name,
        'content': content,
        'url_link': url_link
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
    elif (col == 'url_link'):
        validate_url_link(value)
    else:
        raise Exception("Request params (name / content / url_link) not found")
    
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
