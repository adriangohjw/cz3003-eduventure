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

<<<<<<< HEAD
manager.add_command('db', MigrateCommand)

=======
>>>>>>> 990acf09f6d15bee89bf0c357d57f219d368b3ac
if __name__ == '__main__':
    manager.run()