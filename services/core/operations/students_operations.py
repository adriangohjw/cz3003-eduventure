from models import Student

from .users_operations import initializeUser
from ..dao.StudentsDAO import studentRead, studentCreate
from exceptions import ErrorWithCode

def initializeStudent(email, password, matriculation_number):
    user = initializeUser(email, password)
    if (user and (matriculation_number is not None)):
        return Student(user, matriculation_number)
    else:
        return False

def studentReadOperation(email):
    student = studentRead(col='email', value=email)

    # student is not found
    if student is None:
        raise ErrorWithCode(404, "No student found")

    # success case
    return student

def studentCreateOperation(email, password, matriculation_number):
    student = studentRead(col='email', value=email)

    # if student exist found
    if student:
        raise ErrorWithCode(412, "Existing student")

    student = initializeStudent(email, password, matriculation_number)
    if studentCreate(student) == False:
        raise ErrorWithCode(400, "Unsuccessful")

    # success case
    return student
