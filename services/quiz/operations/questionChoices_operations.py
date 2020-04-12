from models import QuestionChoice

from ..dao.QuestionsDAO import questionRead
from ..dao.QuestionChoicesDAO import \
    questionChoiceCreate, questionChoiceRead, questionChoiceUpdate, questionChoiceDelete, \
    getLastQuestionChoiceID
from exceptions import ErrorWithCode

def initializeQuestionChoice(question_id, description, is_correct):
    question = questionRead(question_id)
    if (question):
        lastQuestionChoiceID = getLastQuestionChoiceID(question_id=question.id)
        return QuestionChoice(question_id, lastQuestionChoiceID+1, description, is_correct)
    else:
        return False

def questionChoiceReadOperation(question_id, id):
    questionChoice = questionChoiceRead(question_id, id)

    # questionChoice is not found
    if questionChoice is None:
        raise ErrorWithCode(404, "No questionChoice found")

    # success case
    return questionChoice

def questionChoiceCreateOperation(question_id, description, is_correct):
    question = questionRead(question_id)

    # question not found
    if question is None:
        raise ErrorWithCode(404, "No question found")

    questionChoice = initializeQuestionChoice(question_id, description, is_correct)
    if questionChoiceCreate(questionChoice) == False:
        raise ErrorWithCode(400, "Unsuccessful")

    # success case
    return questionChoice
    
def questionChoiceUpdateOperation(question_id, questionChoice_id, description, is_correct):
    questionChoice = questionChoiceRead(question_id, questionChoice_id)

    # questionChoice is not found
    if questionChoice is None:
        raise ErrorWithCode(404, "No questionChoice found")

    if description is not None:
        questionChoice.description = description

    if is_correct is not None:
        questionChoice.is_correct = is_correct

    if questionChoiceUpdate() == False:
        raise ErrorWithCode(400, "Unsuccessful")

    # success case
    return questionChoice

def questionChoiceDeleteOperation(question_id, questionChoice_id):
    questionChoice = questionChoiceRead(question_id, questionChoice_id)
    
    # questionChoice is not found
    if questionChoice is None:
        raise ErrorWithCode(404, "No questionChoice found")

    if questionChoiceDelete(question_id, questionChoice_id) == False:
        raise ErrorWithCode(400, "Unsuccessful")

    # success case
    return True
