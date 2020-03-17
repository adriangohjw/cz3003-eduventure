from flask import request

def validate_index(index):
    # if no 'index' found in params
    if (index is None):
        raise Exception("Request params (index) not found")

    # if index params is empty
    if not index: 
        raise Exception("Index is empty")

def courseReadContract(request):    
    index = request.args.get('index')

    validate_index(index)

    return {
        'index': index
    }

def courseCreateContract(request):
    index = request.args.get('index')
    
    validate_index(index)
    
    return {
        'index': index,
    }