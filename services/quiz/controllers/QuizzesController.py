from flask import jsonify, request
from flask_restful import Resource

from flask.helpers import make_response

from ..contracts.quizzes_contracts import \
    quizReadContract, quizCreateContract, quizUpdateContract, quizDeleteContract

from ..operations.quizzes_operations import \
    quizReadOperation, quizCreateOperation, quizUpdateOperation, quizDeleteOperation

from exceptions import ErrorWithCode

import statistics

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
                q['id'], q['name'], q['is_fast'], q['date_start'], q['date_end']
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


class QuizOverallAPI(Resource):

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
        attempts_list = []
        attempts_score_list = []
        for attempt in quiz.attempts:

            attempts_list.append(
                {
                    'id': attempt.id,
                    'created_at': attempt.created_at,
                    'quiz_id': attempt.quiz_id,
                    'score': attempt.score,
                    'student': {
                        'id': attempt.student_id,
                        'name': attempt.student.name,
                        'email': attempt.student.email
                    }
                }
            )
            attempts_score_list.append(attempt.score)

        # if no attempts
        if len(attempts_score_list) == 0:
            return make_response (
                jsonify (
                    id = quiz.id,
                    is_fast = quiz.is_fast,
                    name = quiz.name,
                    date_start = quiz.date_start,
                    date_end = quiz.date_end,
                    staff = {
                        'id': quiz.staff.id,
                        "name": quiz.staff.name
                    },
                    attempts = attempts_list,
                    message = "No attempts recorded at the moment"
                ), 200
            )
        else:
            return make_response (
                jsonify (
                    id = quiz.id,
                    is_fast = quiz.is_fast,
                    name = quiz.name,
                    date_start = quiz.date_start,
                    date_end = quiz.date_end,
                    staff = {
                        'id': quiz.staff.id,
                        "name": quiz.staff.name
                    },
                    attempts = attempts_list,
                    highest_score = max(attempts_score_list),
                    lowest_score = min(attempts_score_list),
                    average_score = statistics.mean(attempts_score_list)
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
    

from ..contracts.rs_quiz_question_contains_contracts import \
    questionMngReadContract, questionMngCreateContract, questionMngDeleteContract

from ..operations.rs_quiz_question_contains_operations import \
    questionMngReadOperation, questionMngCreateOperation, questionMngDeleteOperation

class QuestionManagerAPI(Resource):
    def get(self):
        # contracts
        try:
            q = questionMngReadContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )
        
        # operations
        try:
            quiz = questionMngReadOperation(q['quiz_id'])
        except ErrorWithCode as e:
            return make_response(
                jsonify (
                    error = e.message
                ), e.status_code
            )
        
        # success case
        return make_response(
            jsonify (quiz.asdict_questionMng()), 200
        )

    def post(self):
        # contracts
        try:
            r = questionMngCreateContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            rs = questionMngCreateOperation(
                r['quiz_id'], r['question_id']
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

    def delete(self):
        # contracts
        try:
            r = questionMngDeleteContract(request)
        except Exception as e:
            return make_response(
                jsonify (
                    error = str(e),
                ), 400
            )

        # operations
        try:
            rs = questionMngDeleteOperation(
                r['quiz_id'], r['question_id']
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
                message = 'Successfully deleted quiz'
            ), 200
        )
