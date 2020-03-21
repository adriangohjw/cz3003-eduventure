import unittest 
from flask import Flask
from config import Config

from services.core.dao.tests.test_UsersDao import Test_users_dao

from services.core.contracts.tests.test_users_contracts import Test_user_contracts
from services.core.contracts.tests.test_courses_contracts import Test_courses_contracts
from services.core.contracts.tests.test_lessons_contracts import Test_lessons_contracts
from services.core.contracts.tests.test_questionAttempts_contracts import Test_questionAttempts_contracts
from services.core.contracts.tests.test_quizAttempts_contracts import Test_quizAttempts_contracts
from services.core.contracts.tests.test_students_contracts import Test_students_contracts
from services.core.contracts.tests.test_topics_contracts import Test_topics_contracts

from services.core.operations.tests.test_users_operations import Test_users_operations

from services.quiz.dao.tests.test_QuizzesDao import Test_quizzes_dao

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.URI

    return app

if __name__ == '__main__':
    unittest.main()
