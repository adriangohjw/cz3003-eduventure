from flask import jsonify, request
from flask_restful import Resource

from flask.helpers import make_response

from ..contracts.topics_contracts import \
    topicReadContract, topicCreateContract, topicUpdateContract, topicDeleteContract
from ..operations.topics_operations import \
    topicReadOperation, topicCreateOperation, topicUpdateOperation, topicDeleteOperation, topiclistReadOperation
from exceptions import ErrorWithCode

class TopicAPI(Resource):
    def get(self):
        # contracts
        try:
            t = topicReadContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )
        
        # operations
        try:
            topic = topicReadOperation(t['id'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify (topic.asdict()), 200
        )
        
    def post(self):
        # contracts
        try:
            t = topicCreateContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            topic = topicCreateOperation(t['name'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify(topic.asdict()), 200
        )

    def put(self):
        # contracts
        try:
            t = topicUpdateContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            topic = topicUpdateOperation(
                t['id'], t['name']
            )
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify(topic.asdict()), 200
        )

    def delete(self):
        # contracts
        try:
            t = topicDeleteContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            topic = topicDeleteOperation(
                t['id']
            )
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify(
                message = 'Successfully deleted topic'
            ), 200
        )


class TopicListAPI(Resource):
    def get(self):
        # operations
        try:
            topics = topiclistReadOperation()
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify (
                topics = [topic.asdict() for topic in topics]
            ), 200
        )
