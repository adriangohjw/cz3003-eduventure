from models import Staff

from .users_operations import initializeUser
from ..dao.StaffsDAO import staffRead, staffCreate
from exceptions import ErrorWithCode

def initializeStaff(email, password):
    user = initializeUser(email, password)
    if (user):
        return Staff(user)
    else:
        return False

def staffReadOperation(email):
    staff = staffRead(col='email', value=email)

    # staff is not found
    if staff is None:
        raise ErrorWithCode(404, "No staff found")

    # success case
    return staff

def staffCreateOperation(email, password):
    staff = staffRead(col='email', value=email)

    # if staff exist found
    if staff:
        raise ErrorWithCode(412, "Existing staff")

    staff = initializeStaff(email, password)
    if staffCreate(staff) == False:
        raise ErrorWithCode(400, "Unsuccessful")

    # success case
    return staff
