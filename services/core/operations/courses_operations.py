from models import Course

from ..dao.CoursesDAO import courseRead, courseCreate
from exceptions import ErrorWithCode

def initializeCourse(index):
    if (index is not None):
        return Course(index)
    else:
        return False

def courseReadOperation(index):
    course = courseRead(index)

    # course is not found
    if course is None:
        raise ErrorWithCode(404, "No course found")

    # success case
    return course

def courseCreateOperation(index):
    course = courseRead(index)

    # if course exist found
    if course:
        raise ErrorWithCode(412, "Existing course")

    course = initializeCourse(index)
    if courseCreate(course) == False:
        raise ErrorWithCode(400, "Unsuccessful")

    # success case
    return course
