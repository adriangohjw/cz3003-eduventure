from flask import jsonify, request
from flask_restful import Resource, Api

from models import db, Topic
from flask.helpers import make_response

import requests
import bcrypt

def create_topic(name):
    if (name is not None):
        return Topic(name)
    else:
        return False

def is_topic(name):
    return bool(Topic.query.filter_by(name=name).first())

class TopicAPI(Resource):
    def post(self):
        name = request.args.get('name')
        if (is_topic(name)):
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