from flask import jsonify, request
from flask_restful import Resource

from models import db, Lesson
from flask.helpers import make_response

import json

from ..dao.LessonsDAO import lessonCreate, lessonRead, lessonUpdate
from ..dao.TopicsDAO import topicRead

def initializeLesson(topic_id, name, content):
    topic = topicRead(col='id', value=topic_id)
    if (topic):
        id = len(topic.lessons) + 1
        return Lesson(topic_id, id, name, content)
    else:
        return False

class LessonAPI(Resource):
    def post(self):
        r_json = request.args.get('value')
        r = json.loads(r_json)
        topic_id = r['topic_id']
        name = r['name']
        content = r['content']

        lesson = initializeLesson(topic_id, name, content)
        if (lessonRead(col='name', value=name)):    # lesson already exist
            return make_response(  
                jsonify(
                    message = "Lesson already exist"
                ), 400
            )
        else:   # lesson does not exist
            lesson_create_status = lessonCreate(lesson)
            if (lesson_create_status):  # if lesson creation is successful
                return make_response(
                    jsonify(
                        message = "Lesson creation - successful"
                    ), 200
                )
            else:   # if lesosn creation is unsuccessful
                return make_response(
                    jsonify (
                        message = "Lesson creation - precondition failed"
                    ), 412
                )