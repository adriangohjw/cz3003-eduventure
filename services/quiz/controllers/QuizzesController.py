from flask import jsonify, request
from flask_restful import Resource

from flask.helpers import make_response

from ..contracts.quizzes_contracts import \
    quizReadContract, quizCreateContract, quizUpdateContract, quizDeleteContract

from ..operations.quizzes_operations import \
    quizReadOperation, quizCreateOperation, quizUpdateOperation, quizDeleteOperation

from exceptions import ErrorWithCode

class QuizAPI(Resource):
    def get(self):
        # contracts
        try:
            q = quizReadContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            quiz = quizReadOperation(q['id'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify (quiz.asdict()), 200
        )

    def post(self):
        # contracts
        try:
            q = quizCreateContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            quiz = quizCreateOperation(
                q['staff_id'], q['name'], q['is_fast'], q['date_start'], q['date_end']
            )
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify(quiz.asdict()), 200
        )

    def put(self):
        # contracts
        try:
            q = quizUpdateContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )    
        
        # operations
        try:
            quiz = quizUpdateOperation(
                q['id'], q['col'], q['value']
            )
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify(quiz.asdict()), 200
        )

    def delete(self):
        # contracts
        try:
            q = quizDeleteContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )    
        
        # operations
        try:
            quiz = quizDeleteOperation(q['id'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify(
                message = 'Successfully deleted quiz'
            ), 200
        )


from ..contracts.rs_quiz_course_assigns_contracts import \
    courseMngReadContract, courseMngCreateContract

from ..operations.rs_quiz_course_assigns_operations import \
    courseMngReadOperation, courseMngCreateOperation

class CourseManagerAPI(Resource):
    def get(self):
        # contracts
        try:
            q = courseMngReadContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )
        
        # operations
        try:
            quiz = courseMngReadOperation(q['quiz_id'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify (quiz.asdict_courseMng()), 200
        )

    def post(self):
        # contracts
        try:
            r = courseMngCreateContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            rs = courseMngCreateOperation(
                r['quiz_id'], r['course_index']
            )
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify(rs.asdict()), 200
        )
