from flask import request
import datetime

def validate_id(id):
    # if no 'id' found in params
    if (id is None):
        raise Exception("Request params (id) not found")

    # if 'id' params is empty
    if not id: 
        raise Exception("id is empty")

def validate_col(col):
    # if no 'col' found in params
    if (col is None):
        raise Exception("Request params (col) not found")

    # if field params is empty
    if not col: 
        raise Exception("col is empty")

    if col not in ('name', 'is_fast', 'date_start', 'date_end'):
        raise Exception("Invalid request in params (col)")

def validate_staff_id(staff_id):
    # if no 'staff_id' found in params
    if (staff_id is None):
        raise Exception("Request params (staff_id) not found")

    # if 'staff_id' params is empty
    if not staff_id: 
        raise Exception("staff_id is empty")

def validate_name(name):
    # if no 'name' found in params
    if (name is None):
        raise Exception("Request params (name) not found")

    # if name params is empty
    if not name: 
        raise Exception("name is empty")

def validate_is_fast(is_fast):
    # if no 'is_fast' found in params
    if (is_fast is None):
        raise Exception("Request params is_fast is not found")

    # if is_correct params is empty
    if not is_fast:
        raise Exception("is_fast is empty")

    if is_fast not in ('True', 'False'):
        raise Exception("is_fast is not boolean")

def validate_date_start(date_start):
    # if no 'date_start' found in params
    if (date_start is None):
        raise Exception("Request params date_start is not found")

    # if date_start params is empty
    if not date_start:
        raise Exception("date_start is empty")

    # check if date_start is in the right format
    try:
        datetime.datetime.strptime(date_start, '%Y-%m-%d')
    except:
        raise Exception("date_start is in the wrong format - must be yyyy-mm-dd")

def validate_date_end(date_end):
    # if no 'date_end' found in params
    if (date_end is None):
        raise Exception("Request params date_end is not found")

    # if date_end params is empty
    if not date_end:
        raise Exception("date_end is empty")

    # check if date_end is in the right format
    try:
        datetime.datetime.strptime(date_end, '%Y-%m-%d')
    except:
        raise Exception("date_start is in the wrong format - must be yyyy-mm-dd")

def quizReadContract(request):    
    id = request.args.get('id')

    validate_id(id)

    return {
        'id': id
    }

def quizCreateContract(request):
    staff_id = request.args.get('staff_id')
    name = request.args.get('name')
    is_fast = request.args.get('is_fast')
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
        'is_fast': True if is_fast == 'True' else False,
        'date_start': date_start,
        'date_end': date_end
    }

def quizUpdateContract(request):
    id = request.args.get('id')
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
    elif col == 'date_end':
        validate_date_end(value)
    
    return {
        'id': id,
        'col': col,
        'value': value
    }

def quizDeleteContract(request):
    id = request.args.get('id')

    validate_id(id)

    return {
        'id': id
    }