from flask import request
import re

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

def validate_email(email):
    # if no 'email' found in params
    if (email is None):
        raise TypeError("Request params (email) not found")

    # if email params is empty
    if not email: 
        raise ValueError("Email is empty")

    # if email is in wrong format is empty
    if not EMAIL_REGEX.match(email): 
        raise ValueError("Email format is wrong")

def validate_password(password):
    # if no 'password' found in params
    if (password is None):
        raise TypeError("Request params (password) not found")

    # if password params is empty
    if not password: 
        raise ValueError("Password is empty")

def validate_name(name):
    # if no 'name' found in params
    if (name is None):
        raise TypeError("Request params (name) not found")

    # if name params is empty
    if not name: 
        raise ValueError("Name is empty")

def userReadContract(request):    
    email = request.args.get('email')

    validate_email(email)

    return {
        'email': email,
    }

def userCreateContract(request):
    email = request.args.get('email')
    password = request.args.get('password')

    validate_email(email)
    validate_password(password)

    return {
        'email': email,
        'password': password
    }

def userUpdateContract(request):
    email = request.args.get('email')
    old_password = request.args.get('old_password')
    new_password = request.args.get('new_password')

    validate_email(email)
    validate_password(old_password)
    validate_password(new_password)

    return {
        'email': email,
        'old_password': old_password,
        'new_password': new_password,
    }

def authContract(request):
    email = request.args.get('email')
    password = request.args.get('password')

    validate_email(email)
    validate_password(password)

    return {
        'email': email,
        'password': password
    }
