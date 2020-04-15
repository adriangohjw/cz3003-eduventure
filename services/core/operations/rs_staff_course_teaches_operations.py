from models import Rs_staff_course_teach

from ..dao.StaffsDAO import staffRead
from ..dao.CoursesDAO import courseRead
from ..dao.RsStaffCourseTeachDAO import rsStaffCourseTeachRead, rsStaffCourseTeachCreate
from exceptions import ErrorWithCode

def initializeRsStaffCourseTeach(staff_id, course_index):
    if ((staff_id is not None) and (course_index is not None)):
        return Rs_staff_course_teach(staff_id, course_index)
    else:
        return False

def courseMngReadOperation(user_email):
    staff = staffRead(col='email', value=user_email)

    # staff is not found
    if staff is None:
        raise ErrorWithCode(409, "No staff found")

    # success case
    return staff

def courseMngCreateOperation(user_email, course_index):
    staff = staffRead(col='email', value=user_email)
    course = courseRead(course_index)

    # staff is not found
    if staff is None:
        raise ErrorWithCode(409, "No staff found")

    # course is not found
    if course is None:
        raise ErrorWithCode(409, "No course found")

    rs = rsStaffCourseTeachRead(staff.id, course.index)

    # if rs exist
    if rs is not None:
        raise ErrorWithCode(409, "Existing rs")

    rs = initializeRsStaffCourseTeach(staff.id, course.index)
    if rsStaffCourseTeachCreate(rs) == False:
        raise ErrorWithCode(503, "Unsuccessful")

    # success case
    return rs
