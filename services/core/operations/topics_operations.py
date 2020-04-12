from models import Topic

from ..dao.TopicsDAO import topicCreate, topicRead, topiclistRead
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
        raise ErrorWithCode(404, "No topic found")

    # success case
    return topic

def topicCreateOperation(name):
    topic = topicRead(col='name', value=name)

    # if topic exist found
    if topic:
        raise ErrorWithCode(412, "Existing topic")

    topic = initializeTopic(name)
    if topicCreate(topic) == False:
        raise ErrorWithCode(400, "Unsuccessful")

    # success case
    return topic

def topiclistReadOperation():
    return topiclistRead()
    