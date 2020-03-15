from flask import jsonify, request
from flask_restful import Resource

from models import db, Topic
from flask.helpers import make_response

import requests

def create_topic(name):
    if (name is not None):
        return Topic(name)
    else:
        return False

def is_topic(col, value):
    if (col == 'name'):
        return bool(Topic.query.filter_by(name=value).first())
    elif (col == 'id'):
        return bool(Topic.query.filter_by(id=value).first())

def getTopic(col, value):
    if (is_topic(col=col, value=value)):
        if (col == 'name'):
            return Topic.query.filter_by(name=value).first()
        elif (col == 'id'):
            return Topic.query.filter_by(id=value).first()
    else:
        return False

class TopicAPI(Resource):
    def get(self):
        id = request.args.get('id')
        topic = getTopic(col='id', value=id)
        if (topic):
            print(len(topic.lessons))
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
        if (is_topic('name', name)):
            return make_response(
                jsonify(
                    message = "Topic already exist"
                ), 400
            )
        topic = create_topic(name)
        if (topic):
            db.session.add(topic)
            db.session.commit()
            return make_response(
                jsonify(
                    message = "Topic creation - successful"
                ), 200
            )
        else:  
            return make_response(
                jsonify (
                    message = "Topic creation - precondition failed"
                ), 412
            )