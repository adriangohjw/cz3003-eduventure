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
    def get(self):
        topic_id = request.args.get('topic_id')
        lesson_id = request.args.get('lesson_id')
        lesson = lessonRead(topic_id=topic_id, col='id', value=lesson_id)
        if (lesson):    # if lesson can be found   
            return make_response(
                jsonify (
                    topic_id = lesson.topic_id,
                    id = lesson.id,
                    name = lesson.name,
                    content = lesson.content,
                    count_questions = len(lesson.questions),
                    questions = lesson.questions
                ), 200
            )
        else:   # if lesson cannot be found
            return make_response(
                jsonify (
                    message = "no lesson found"
                ), 404
            )

    def post(self):
        r_json = request.args.get('value')
        r = json.loads(r_json)
        try:
            topic_id = r['topic_id']
            name = r['name']
            content = r['content']
            lesson = initializeLesson(topic_id, name, content)

            if (lessonRead(topic_id=topic_id, col='name', value=name)):    # lesson already exist
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
        except KeyError as e:
            print(e)
            return make_response(
                jsonify (
                    message = "Incorrect parameters passed"
                ), 412
            )