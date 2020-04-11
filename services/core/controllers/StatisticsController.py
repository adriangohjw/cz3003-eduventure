from flask import jsonify, request
from flask_restful import Resource

from flask.helpers import make_response

"""
from services.core.contracts.statistics_contracts import \
    statReadContract
"""

from services.core.operations.statistics_operations import \
    statReadOperation, lessonCompletedReadOperation, leaderboardReadOperation

from exceptions import ErrorWithCode


class Stats_API(Resource):

    def get(self):
        # operations
        try:
            stat = statReadOperation()
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify (stat), 200
        )


class Lesson_Completion_API(Resource):

    def get(self):
        # operations
        try:
            stat = lessonCompletedReadOperation()
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify (stat), 200
        )

class LeaderBoard_API(Resource):

    def get(self):
        # operations
        try:
            stat = leaderboardReadOperation()
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify (stat), 200
        )
    