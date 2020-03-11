from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = Config.URI
api = Api(app)
db = SQLAlchemy(app)

class HelloWorld(Resource):
    def get(self):
        return jsonify(
            about = "Hello world!"
        )

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(port=5000, debug=True)