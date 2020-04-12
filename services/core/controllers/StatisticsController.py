from flask import jsonify, request
from flask_restful import Resource

from flask.helpers import make_response

from services.core.contracts.statistics_contracts import \
    leaderboardReadContract, studentScoreReadContract, courseScoreReadContract, activityReadContract

from services.core.operations.statistics_operations import \
    statReadOperation, lessonCompletedReadOperation, leaderboardReadOperation, \
    studentScoreReadOperation, courseScoreReadOperation, activityReadOperation

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
        # contracts
        try:
            s = leaderboardReadContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            stat = leaderboardReadOperation(
                s['student_id']
            )
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

class StudentScore_API(Resource):

    def get(self):
        # contracts
        try:
            s = studentScoreReadContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            stat = studentScoreReadOperation(
                s['student_id']
            )
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


class CourseScore_API(Resource):

    def get(self):
        # contracts
        try:
            s = courseScoreReadContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            stat = courseScoreReadOperation(
                s['course_index']
            )
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


class Activity_API(Resource):

    def get(self):
        # contracts
        try:
            s = activityReadContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            stat = activityReadOperation(
                s['date_start'], s['date_end'], s['student_id']
            )
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
