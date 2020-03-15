from flask import jsonify, request
from flask_restful import Resource, reqparse

from models import db, Lesson
from flask.helpers import make_response

import requests
import json

from .TopicsController import is_topic, getTopic

def create_lesson(topic_id, name, content):
    if (is_topic(col='id', value=topic_id)):
        topic = getTopic(col='id', value=topic_id)
        id = len(topic.lessons) + 1
        return Lesson(topic_id, id, name, content)
    else:
        return False

def is_lesson(name):
    return bool(Lesson.query.filter_by(name=name).first())

class LessonAPI(Resource):
    def post(self):
        r_json = request.args.get('value')
        r = json.loads(r_json)
        topic_id = r['topic_id']
        name = r['name']
        content = r['content']

        if (is_lesson(name)):
            return make_response(
                jsonify(
                    message = "Lesson already exist"
                ), 400
            )
            
        lesson = create_lesson(topic_id, name, content)
        if (lesson):
            db.session.add(lesson)
            db.session.commit()
            return make_response(
                jsonify(
                    message = "Lesson creation - successful"
                ), 200
            )
        else:  
            return make_response(
                jsonify (
                    message = "Lesson creation - precondition failed"
                ), 412
            )