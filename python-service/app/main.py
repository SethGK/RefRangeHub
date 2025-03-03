from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import SECRET_KEY, DEBUG, SQLALCHEMY_DATABASE_URI
from app.auth_routes import auth_bp
from app.routes import test_bp

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['DEBUG'] = DEBUG
    app.config['JWT_SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    jwt = JWTManager(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(test_bp, url_prefix='/api')

    # Error handler inside create_app()
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal Server Error"}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
