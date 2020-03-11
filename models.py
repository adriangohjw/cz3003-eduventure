from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import Config

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = DB_conn.URI
db = SQLAlchemy(app)