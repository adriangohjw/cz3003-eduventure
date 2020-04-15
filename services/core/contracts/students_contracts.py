from flask import request

from .users_contracts import validate_email, validate_password, validate_name

def validate_matriculation_number(matriculation_number):
    # if no 'matriculation_number' found in params
    if (matriculation_number is None):
        raise TypeError("Request params (matriculation_number) not found")

    # if password params is empty
    if not matriculation_number: 
        raise ValueError("Matriculation Number is empty")

def studentReadContract(request):    
    email = request.args.get('email')

    validate_email(email)

    return {
        'email': email,
    }

def studentCreateContract(request):
    email = request.args.get('email')
    password = request.args.get('password')
    matriculation_number = request.args.get('matriculation_number')
    name = request.args.get('name')
    
    validate_email(email)
    validate_password(password)
    validate_matriculation_number(matriculation_number)
    if name is not None:
        validate_name(name)
    
    return {
        'email': email,
        'password': password,
        'matriculation_number': matriculation_number,
        'name': name
    }