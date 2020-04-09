from models import Quiz

from ...core.dao.StaffsDAO import staffRead
from ..dao.QuizzesDAO import quizCreate, quizRead, quizUpdate, quizDelete
from exceptions import ErrorWithCode

def initializeQuiz(staff_id, name, is_fast, date_start, date_end):
    return Quiz(staff_id, name, is_fast, date_start, date_end)

# end date before start date
def validate_dates(date_start, date_end):
    if date_end < date_start:
        raise ErrorWithCode(412, "End date before start date")

def quizReadOperation(id):
    quiz = quizRead(id)

    # quiz is not found
    if quiz is None:
        raise ErrorWithCode(404, "No quiz found")

    # success case
    return quiz

def quizCreateOperation(staff_id, name, is_fast, date_start, date_end):
    staff = staffRead(col='id', value=staff_id)
    
    # staff not found
    if staff is None:
        raise ErrorWithCode(404, "No staff found")

    validate_dates(date_start, date_end)

    quiz = initializeQuiz(staff_id, name, is_fast, date_start, date_end)
    if quizCreate(quiz) == False:
        raise ErrorWithCode(400, "Unsuccessful")

    # success case
    return quiz
    
def quizUpdateOperation(id, name, is_fast, date_start, date_end):
    quiz = quizRead(id)

    # quiz is not found
    if quiz is None:
        raise ErrorWithCode(404, "No quiz found")

    if name is not None:
        quiz.name = name
    
    if is_fast is not None:
        quiz.is_fast = is_fast

    if (date_start is not None) and (date_end is not None):
        validate_dates(date_start, date_end)
        quiz.date_start = date_start
        quiz.date_end = date_end
    else:
        if (date_start is not None):
            validate_dates(date_start, quiz.date_end)
            quiz.date_start = date_start
        elif (date_end is not None):
            validate_dates(quiz.date_start, date_end)
            quiz.date_end = date_end

    if quizUpdate() == False:
        raise ErrorWithCode(400, "Unsuccessful")

    # success case
    return quiz

def quizDeleteOperation(id):
    quiz = quizRead(id)
    
    # quiz is not found
    if quiz is None:
        raise ErrorWithCode(404, "No quiz found")

    if quizDelete(id) == False:
        raise ErrorWithCode(400, "Unsuccessful")

    # success case
    return True