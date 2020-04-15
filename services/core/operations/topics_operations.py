from models import Topic

from ..dao.TopicsDAO import topicCreate, topicRead, topicUpdate, topicDelete, topiclistRead
from services.core.dao.LessonsDAO import lessonListRead
from exceptions import ErrorWithCode

def initializeTopic(name):
    if (name is not None):
        return Topic(name)
    else:
        return False

def topicReadOperation(id):
    topic = topicRead(col='id', value=id)

    # topic is not found
    if topic is None:
        raise ErrorWithCode(409, "No topic found")

    # success case
    return topic

def topicCreateOperation(name):
    topic = topicRead(col='name', value=name)

    # if topic exist found
    if topic:
        raise ErrorWithCode(409, "Existing topic")

    topic = initializeTopic(name)
    if topicCreate(topic) == False:
        raise ErrorWithCode(503, "Unsuccessful")

    # success case
    return topic

def topicUpdateOperation(id, name):
    topic = topicRead(col='id', value=id)

    # if topic not found
    if topic is None:
        raise ErrorWithCode(409, "No topic found")

    topic.name = name

    if topicUpdate() is False:
        raise ErrorWithCode(503, "Unsuccessful")

    # success case
    return topic

def topicDeleteOperation(id):

    topic = topicRead(col='id', value=id)

    # if topic not found
    if topic is None:
        raise ErrorWithCode(409, "No topic found")

    lessons = lessonListRead()
    for lesson in lessons:
        if lesson.topic_id == id:
            raise ErrorWithCode(409, "Topic has lessons assigned to it")

    if topicDelete(id) == False:
        raise ErrorWithCode(503, "Unsuccessful")

    # success case
    return True

def topiclistReadOperation():
    return topiclistRead()
    