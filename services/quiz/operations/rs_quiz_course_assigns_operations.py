from models import Rs_quiz_course_assign

from ...core.dao.CoursesDAO import courseRead
from ..dao.QuizzesDAO import quizRead
from ..dao.RsQuizCourseAssignDAO import rsQuizCourseAssignRead, rsQuizCourseAssignCreate
from exceptions import ErrorWithCode

def initializeRsQuizCourseAssign(quiz_id, course_index):
    return Rs_quiz_course_assign(
        quiz_id = quiz_id,
        course_index = course_index
    )

def courseMngReadOperation(quiz_id):
    quiz = quizRead(quiz_id)

    # staff is not found
    if quiz is None:
        raise ErrorWithCode(404, "No quiz found")

    # success case
    return quiz

def courseMngCreateOperation(quiz_id, course_index):
    quiz = quizRead(quiz_id)
    course = courseRead(course_index)

    # quiz is not found
    if quiz is None:
        raise ErrorWithCode(404, "No quiz found")

    # course is not found
    if course is None:
        raise ErrorWithCode(404, "No course found")

    rs = rsQuizCourseAssignRead(quiz.id, course.index)

    # if rs exist
    if rs is not None:
        raise ErrorWithCode(412, "Existing rs")

    rs = initializeRsQuizCourseAssign(quiz.id, course.index)
    if rsQuizCourseAssignCreate(rs) == False:
        raise ErrorWithCode(400, "Unsuccessful")

    # success case
    return rs
