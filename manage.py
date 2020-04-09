from models import db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from run import create_app

app = create_app()
db.init_app(app)
migrate = Migrate(app, db, compare_type=True)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
    