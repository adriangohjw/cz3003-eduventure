from flask import Flask
from config import Config
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.URI

    return app

if __name__ == "__main__":
    app = create_app()

    from models import db 
    db.init_app(app)

    from services.core.app import user_bp, staff_bp
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(staff_bp, url_prefix='/staffs')

    app.run(port=5000, debug=True)