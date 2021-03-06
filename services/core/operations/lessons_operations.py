from models import Lesson

from ..dao.TopicsDAO import topicRead
from ..dao.LessonsDAO import lessonRead, lessonCreate, lessonUpdate, lessonDelete, lessonListRead, getLastLessonID
from exceptions import ErrorWithCode

def initializeLesson(topic_id, name, content, url_link):
    topic = topicRead(col='id', value=topic_id)
    if (topic):
        lastLessonID = getLastLessonID(topic_id=topic.id)
        return Lesson(topic_id, lastLessonID+1, name, content, url_link)
    else:
        return False

def lessonReadOperation(topic_id, lesson_id):
    lesson = lessonRead(topic_id=topic_id, col='id', value=lesson_id)

    # lesson is not found
    if lesson is None:
        raise ErrorWithCode(409, "No lesson found")

    # success case
    return lesson

def lessonCreateOperation(topic_id, name, content, url_link):
    lesson = lessonRead(topic_id=topic_id, col='name', value=name)

    # if lesson exist found
    if lesson:
        raise ErrorWithCode(409, "Existing lesson")

    lesson = initializeLesson(topic_id=topic_id, name=name, content=content, url_link=url_link)
    if lessonCreate(lesson) == False:
        raise ErrorWithCode(503, "Unsuccessful")

    # success case
    return lesson
    
def lessonUpdateOperation(topic_id, lesson_id, col, value):
    lesson = lessonRead(topic_id=topic_id, col='id', value=lesson_id)

    # lesson is not found
    if lesson is None:
        raise ErrorWithCode(409, "No lesson found")

    if (col == 'name'):
        lesson.name = value
    elif (col == 'content'):
        lesson.content = value
    elif (col == 'url_link'):
        lesson.url_link = value

    if lessonUpdate() == False:
        raise ErrorWithCode(503, "Unsuccessful")

    # success case
    return lesson

def lessonDeleteOperation(topic_id, lesson_id):
    lesson = lessonRead(topic_id=topic_id, col='id', value=lesson_id)
    
    # lesson is not found
    if lesson is None:
        raise ErrorWithCode(409, "No lesson found")

    if lessonDelete(topic_id, lesson_id) == False:
        raise ErrorWithCode(503, "Unsuccessful")

    # success case
    return True

def lessonListReadOperation():
    return lessonListRead()
    