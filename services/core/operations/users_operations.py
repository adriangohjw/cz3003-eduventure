import bcrypt
from models import User

from ..dao.UsersDAO import userRead, userCreate, userUpdate
from exceptions import ErrorWithCode

def encrypt(plaintext_password):
    return bcrypt.hashpw(bytes(plaintext_password, "utf8"), bcrypt.gensalt()).decode("utf-8")

def authenticate(plaintext_password, encrypted_password):
    return bcrypt.checkpw(bytes(plaintext_password, "utf-8"), bytes(encrypted_password, "utf-8"))

def initializeUser(email, password):
    email_split = email.split('@')
    name = email_split[0]
    encrypted_password = encrypt(password)
    if (len(email_split) == 2) and (password is not None):
        return User(
            email=email, 
            name=name, 
            encrypted_password=encrypted_password
        )
    else:
        return False

def userReadOperation(email):
    user = userRead(col='email', value=email)

    # user is not found
    if user is None:
        raise ErrorWithCode(404, "No user found")

    # success case
    return user

def userCreateOperation(email, password):
    user = userRead(col='email', value=email)

    # if user exist found
    if user:
        raise ErrorWithCode(412, "Existing user")

    user = initializeUser(email, password)
    if userCreate(user) == False:
        raise ErrorWithCode(400, "Unsuccessful")

    # success case
    return user

def userUpdateOperation(email, old_password, new_password):
    user = userRead(col='email', value=email)

    # user is not found
    if user is None:
        raise ErrorWithCode(404, "No user found")

    # password authentication fail
    if authenticate(old_password, user.encrypted_password) == False:
        raise ErrorWithCode(401, "Wrong password does not match")

    user.encrypted_password = encrypt(new_password)
    if userUpdate(user) == False:
        raise ErrorWithCode(400, "Unsuccessful")

    # success case
    return user
