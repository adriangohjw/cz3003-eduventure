from flask import Blueprint
from flask_restful import Resource, Api
from config import Config

from services.core.resources import UsersController

user_bp = Blueprint('user', __name__)
api_user = Api(user_bp)
api_user.add_resource(UsersController.UserAPI, '/')