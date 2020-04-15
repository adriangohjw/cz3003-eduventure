from models import Staff

from .users_operations import initializeUser
from ..dao.StaffsDAO import staffRead, staffCreate
from exceptions import ErrorWithCode

def initializeStaff(email, password, name):
    user = initializeUser(email, password, name)
    return Staff(user)

def staffReadOperation(email):
    staff = staffRead(col='email', value=email)

    # staff is not found
    if staff is None:
        raise ErrorWithCode(409, "No staff found")

    # success case
    return staff

def staffCreateOperation(email, password, name):
    staff = staffRead(col='email', value=email)

    # if staff exist found
    if staff:
        raise ErrorWithCode(409, "Existing staff")

    staff = initializeStaff(email, password, name)
    if staffCreate(staff) == False:
        raise ErrorWithCode(503, "Unsuccessful")

    # success case
    return staff
