from models import Student

from .users_operations import initializeUser
from ..dao.StudentsDAO import studentRead, studentCreate
from exceptions import ErrorWithCode

def initializeStudent(email, password, matriculation_number, name):
    user = initializeUser(email, password, name)
    return Student(user, matriculation_number)

def studentReadOperation(email):
    student = studentRead(col='email', value=email)

    # student is not found
    if student is None:
        raise ErrorWithCode(409, "No student found")

    # success case
    return student

def studentCreateOperation(email, password, matriculation_number, name):
    student = studentRead(col='email', value=email)

    # if student exist found
    if student:
        raise ErrorWithCode(409, "Existing student")

    student = initializeStudent(email, password, matriculation_number, name)
    if studentCreate(student) == False:
        raise ErrorWithCode(503, "Unsuccessful")

    # success case
    return student
