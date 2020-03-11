from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import Config

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = Config.URI
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)

if __name__ == '__main__':
    manager.run()