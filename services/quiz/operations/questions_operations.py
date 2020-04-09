import sys
from os import path, getcwd
sys.path.append(getcwd())

from models import Question

from ...core.dao.LessonsDAO import lessonRead
from ..dao.QuestionsDAO import questionCreate, questionRead, questionUpdate, questionDelete, questionGetAllRead
from ...core.dao.LessonsDAO import lessonRead
from exceptions import ErrorWithCode

def initializeQuestion(topic_id, lesson_id, description):
    return Question(topic_id, lesson_id, description)

def questionReadOperation(id):
    question = questionRead(id)

    # question is not found
    if question is None:
        raise ErrorWithCode(404, "No question found")

    # success case
    return question

def questionCreateOperation(topic_id, lesson_id, description):
    lesson = lessonRead(topic_id=topic_id, col='id', value=lesson_id)

    # topic and lesson not found
    if lesson is None:
        raise ErrorWithCode(404, "No topic/lesson found")

    question = initializeQuestion(topic_id, lesson_id, description)
    if questionCreate(question) == False:
        raise ErrorWithCode(400, "Unsuccessful")

    # success case
    return question
    
def questionUpdateOperation(id, description):
    question = questionRead(id)

    # question is not found
    if question is None:
        raise ErrorWithCode(404, "No question found")

    question.description = description
    if questionUpdate() == False:
        raise ErrorWithCode(400, "Unsuccessful")

    # success case
    return question

def questionDeleteOperation(id):
    question = questionRead(id)
    
    # question is not found
    if question is None:
        raise ErrorWithCode(404, "No question found")

    if questionDelete(id) == False:
        raise ErrorWithCode(400, "Unsuccessful")

    # success case
    return True

def questionGetAllReadOperation():

    questions = questionGetAllRead()

    # success case
    return questions
