from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from config import Config

class HelloWorld(Resource):
    def get(self):
        return jsonify(
            about = "Hello world!"
        )