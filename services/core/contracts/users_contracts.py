from flask import request
import re

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

def validate_email(email):
    # if no 'email' found in params
    if (email is None):
        raise Exception("Request params (email) not found")

    # if email params is empty
    if not email: 
        raise Exception("Email is empty")

    # if email is in wrong format is empty
    if not EMAIL_REGEX.match(email): 
        raise Exception("Email format is wrong")

def validate_password(password):
    # if no 'password' found in params
    if (password is None):
        raise Exception("Request params (password) not found")

    # if password params is empty
    if not password: 
        raise Exception("Password is empty")

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