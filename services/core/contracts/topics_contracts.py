from flask import request

def validate_id(id):
    # if no 'id' found in params
    if (id is None):
        raise TypeError("Request params (id) not found")

    # check if id is a boolean
    # to check if bool before int because isinstance(id, int) returns True if id is bool
    if isinstance(id, bool):
        raise TypeError("Id is not an integer")

    # check if type is integer
    if not isinstance(id, int):
        raise TypeError("Id is not an integer")

def validate_name(name):
    # if no 'name' found in params
    if (name is None):
        raise TypeError("Request params (name) not found")

    # if name params is empty
    if not name: 
        raise ValueError("Name is empty")

def topicReadContract(request):    
    id = request.args.get('id', type=int)

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

def topicUpdateContract(request):
    id = request.args.get('id', type=int)
    name = request.args.get('name')
    
    validate_id(id)
    validate_name(name)
    
    return {
        'id': id,
        'name': name,
    }

def topicDeleteContract(request):
    id = request.args.get('id', type=int)

    validate_id(id)

    return {
        'id': id
    }
