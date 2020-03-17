from ..dao.UsersDAO import userRead
from exceptions import ErrorWithCode

def userReadOperation(email):
    user = userRead(col='email', value=email)

    # user is not found
    if user is None:
        raise ErrorWithCode(404, "No user found")

    # success case
    return {
        'email': user.email,
        'encrypted_password': user.encrypted_password,
        'name': user.name
    }