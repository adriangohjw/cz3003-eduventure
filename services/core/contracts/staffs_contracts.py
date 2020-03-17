from flask import request

from .users_contracts import validate_email, validate_password

def staffReadContract(request):    
    email = request.args.get('email')

    validate_email(email)

    return {
        'email': email,
    }

def staffCreateContract(request):
    email = request.args.get('email')
    password = request.args.get('password')
    
    validate_email(email)
    validate_password(password)
    
    return {
        'email': email,
        'password': password
    }