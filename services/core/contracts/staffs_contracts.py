from flask import request

from .users_contracts import validate_email, validate_password, validate_name

    
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
    if name is not None:
        validate_name(name)
    
    return {
        'email': email,
        'password': password,
        'name': name
    }