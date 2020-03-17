from flask import request
import re

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

def userReadContract(request):    
    email = request.args.get('email')

    # if no 'email' found in params
    if (email is None):
        raise Exception("Request params (email) not found")

    # if email params is empty
    if not email: 
        raise Exception("Email is empty")

    # if email is in wrong format is empty
    if not EMAIL_REGEX.match(email): 
        raise Exception("Email format is wrong")

    # success case
    name = email.split('@')[0]
    return {
        'email': email,
        'name': name
    }