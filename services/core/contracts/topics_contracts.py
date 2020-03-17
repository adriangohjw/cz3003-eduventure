from flask import request

def validate_id(id):
    # if no 'id' found in params
    if (id is None):
        raise Exception("Request params (id) not found")

    # if id params is empty
    if not id: 
        raise Exception("Id is empty")

    if isinstance(id, int) == False:
        raise Exception("Id is not an integer")

def validate_name(name):
    # if no 'name' found in params
    if (name is None):
        raise Exception("Request params (name) not found")

    # if name params is empty
    if not name: 
        raise Exception("Name is empty")

def topicReadContract(request):    
    id = request.args.get('id')

    validate_id(id)

    return {
        'id': id
    }

def topicCreateContract(request):
    name = request.args.get('name')
    
    validate_name(name)
    
    return {
        'name': name,
    }