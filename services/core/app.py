from flask import Blueprint
from flask_restful import Resource, Api
from config import Config

from services.core.resources import UsersController, StaffsController

user_bp = Blueprint('user', __name__)
api_user = Api(user_bp)
api_user.add_resource(UsersController.UserAPI, '/')
api_user.add_resource(UsersController.UserResetPasswordAPI, '/reset_password')

staff_bp = Blueprint('staff', __name__)
api_staff = Api(staff_bp)
api_staff.add_resource(StaffsController.StaffAPI, '/')