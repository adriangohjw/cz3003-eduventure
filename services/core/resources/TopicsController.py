from flask import jsonify, request
from flask_restful import Resource

from models import Topic
from flask.helpers import make_response

from ..dao.TopicsDAO import topicCreate, topicRead, topicUpdate

def initializeTopic(name):
    if (name is not None):
        return Topic(name)
    else:
        return False

class TopicAPI(Resource):
    def get(self):
        id = request.args.get('id')
        topic = topicRead(col='id', value=id)
        if (topic):
            return make_response(
                jsonify(
                    message = "Topic found",
                    count_lessons = len(topic.lessons),
                    lessons = topic.lessons
                ), 200
            )
        else:
            return make_response(
                jsonify(
                    message = "Topic does not exist"
                ), 404
            )
        
    def post(self):
        name = request.args.get('name')
        topic = initializeTopic(name)
        if (topicRead(col='name', value=name)): # topic already exist
            return make_response(
                jsonify(
                    message = "Topic already exist"
                ), 400
            )
        else:
            topic_create_status = topicCreate(topic)
            if (topic_create_status):   # if topic creation is successful
                return make_response(
                    jsonify(
                        message = "Topic creation - successful"
                    ), 200
                )
            else:   # if topic creation is unsuccessful
                return make_response(
                    jsonify (
                        message = "Topic creation - precondition failed"
                    ), 412
                )