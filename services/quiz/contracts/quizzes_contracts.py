from flask import request
import datetime

def validate_id(id):
    # if no 'id' found in params
    if (id is None):
        raise TypeError("Request params (id) not found")

    # if 'id' params is empty
    if not id: 
        raise ValueError("id is empty")

    # check if type is integer
    if not isinstance(id, int):
        raise TypeError("Id is not an integer")

def validate_col(col):
    # if no 'col' found in params
    if (col is None):
        raise TypeError("Request params (col) not found")

    # if field params is empty
    if not col: 
        raise ValueError("col is empty")

    if col not in ('name', 'is_fast', 'date_start', 'date_end'):
        raise ValueError("Invalid request in params (col)")

def validate_staff_id(staff_id):
    # if no 'staff_id' found in params
    if (staff_id is None):
        raise TypeError("Request params (staff_id) not found")

    # if 'staff_id' params is empty
    if not staff_id: 
        raise ValueError("staff_id is empty")

    # check if type is integer
    if not isinstance(staff_id, int):
        raise TypeError("staff_id is not an integer")

def validate_name(name):
    # if no 'name' found in params
    if (name is None):
        raise TypeError("Request params (name) not found")

    # if name params is empty
    if not name: 
        raise ValueError("name is empty")

def validate_is_fast(is_fast):
    # if no 'is_fast' found in params
    if (is_fast is None):
        raise TypeError("Request params is_fast is not found")

    # if is_correct params is empty
    if not is_fast:
        raise ValueError("is_fast is empty")

    # check if type is boolean
    if not isinstance(is_fast, bool):
        raise TypeError("is_fast is not an boolean")

def validate_date_start(date_start):
    # if no 'date_start' found in params
    if (date_start is None):
        raise TypeError("Request params date_start is not found")

    # if date_start params is empty
    if not date_start:
        raise ValueError("date_start is empty")

    # check if date_start is in the right format
    try:
        datetime.datetime.strptime(date_start, '%Y-%m-%d')
    except:
        raise ValueError("date_start is in the wrong format - must be yyyy-mm-dd")

def validate_date_end(date_end):
    # if no 'date_end' found in params
    if (date_end is None):
        raise TypeError("Request params date_end is not found")

    # if date_end params is empty
    if not date_end:
        raise ValueError("date_end is empty")

    # check if date_end is in the right format
    try:
        datetime.datetime.strptime(date_end, '%Y-%m-%d')
    except:
        raise ValueError("date_start is in the wrong format - must be yyyy-mm-dd")

def quizReadContract(request):    
    id = request.args.get('id', type=int)

    validate_id(id)

    return {
        'id': id
    }

def quizCreateContract(request):
    staff_id = request.args.get('staff_id', type=int)
    name = request.args.get('name')
    is_fast = request.args.get('is_fast', type=bool)
    date_start = request.args.get('date_start')
    date_end = request.args.get('date_end')
    
    validate_staff_id(staff_id)
    validate_name(name)
    validate_is_fast(is_fast)
    validate_date_start(date_start)
    validate_date_end(date_end)
    
    return {
        'staff_id': staff_id,
        'name': name,
        'is_fast': is_fast,
        'date_start': datetime.datetime.strptime(date_start, '%Y-%m-%d'),
        'date_end': datetime.datetime.strptime(date_end, '%Y-%m-%d')
    }

def quizUpdateContract(request):
    id = request.args.get('id', type=int)
    col = request.args.get('col')
    value = request.args.get('value')

    validate_id(id)
    validate_col(col)

    if col == 'name':
        validate_name(value)
    elif col == 'is_fast':
        validate_is_fast(value)
        value = True if value == 'True' else False
    elif col == 'date_start':
        validate_date_start(value)
        value = datetime.datetime.strptime(value, '%Y-%m-%d')
    elif col == 'date_end':
        validate_date_end(value)
        value = datetime.datetime.strptime(value, '%Y-%m-%d')
    
    return {
        'id': id,
        'col': col,
        'value': value
    }

def quizDeleteContract(request):
    id = request.args.get('id', type=int)

    validate_id(id)

    return {
        'id': id
    }