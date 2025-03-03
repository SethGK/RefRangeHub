from flask import Flask
from flask_jwt_extended import JWTManager
from app.config import SECRET_KEY, DEBUG
from app.database import engine
from app.models import Base
from app.auth_routes import auth_bp
from routes import test_bp 

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['DEBUG'] = DEBUG
    app.config['JWT_SECRET_KEY'] = SECRET_KEY 

    
    jwt = JWTManager(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(test_bp, url_prefix='/api')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
