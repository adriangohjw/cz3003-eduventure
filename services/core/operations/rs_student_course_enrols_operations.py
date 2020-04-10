from models import Rs_student_course_enrol

from ..dao.StudentsDAO import studentRead
from ..dao.CoursesDAO import courseRead
from ..dao.RsStudentCourseEnrolDAO import rsStudentCourseEnrolRead, rsStudentCourseEnrolCreate
from exceptions import ErrorWithCode

def initializeRsStudentCourseEnrol(student_id, course_index):
    if ((student_id is not None) and (course_index is not None)):
        return Rs_student_course_enrol(student_id, course_index)
    else:
        return False

def courseMngReadOperation(user_email):
    student = studentRead(col='email', value=user_email)

    # student is not found
    if student is None:
        raise ErrorWithCode(404, "No student found")

    # success case
    return student

def courseMngCreateOperation(user_email, course_index):
    student = studentRead(col='email', value=user_email)
    course = courseRead(course_index)

    # student is not found
    if student is None:
        raise ErrorWithCode(404, "No student found")

    # course is not found
    if course is None:
        raise ErrorWithCode(404, "No course found")

    rs = rsStudentCourseEnrolRead(student.id, course.index)

    # if rs exist
    if rs is not None:
        raise ErrorWithCode(412, "Existing rs")

    rs = initializeRsStudentCourseEnrol(student.id, course.index)
    if rsStudentCourseEnrolCreate(rs) == False:
        raise ErrorWithCode(400, "Unsuccessful")

    # success case
    return rs


from services.core.dao.RsStudentCourseEnrolDAO import rsCourseEnrolRead

def courseClasslistReadOperation(course_index):

    # course is not found
    if courseRead(course_index) is None:
        raise ErrorWithCode(404, "No course found")

    rss = rsCourseEnrolRead(course_index)

    # success case
    return rss
