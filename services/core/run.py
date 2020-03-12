from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config['SECURITY_PASSWORD_SALT'] = Config.salt
    
    from app import user_bp
    app.register_blueprint(user_bp, url_prefix='/users')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=5000, debug=True)