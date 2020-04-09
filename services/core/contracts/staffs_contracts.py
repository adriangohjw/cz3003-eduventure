from flask import request

from .users_contracts import validate_email, validate_password

def validate_name(name):
    # if no 'name' found in params
    if (name is None):
        raise TypeError("Request params (name) not found")

    # if name params is empty
    if not name: 
        raise ValueError("Name is empty")
    
def staffReadContract(request):    
    email = request.args.get('email')

    validate_email(email)

    return {
        'email': email,
    }

def staffCreateContract(request):
    email = request.args.get('email')
    password = request.args.get('password')
    name = request.args.get('name')
    
    validate_email(email)
    validate_password(password)
    validate_name(name)
    
    return {
        'email': email,
        'password': password,
        'name': name
    }