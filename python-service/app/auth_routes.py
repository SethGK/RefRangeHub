from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.models import User
from app.database import SessionLocal
from datetime import timedelta
from app.schemas import RegisterSchema, LoginSchema
from marshmallow import ValidationError

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    session = SessionLocal()
    try:
        json_data = request.get_json()
        # Validate input data using RegisterSchema
        schema = RegisterSchema()
        data = schema.load(json_data)
        
        # Check if user already exists
        if session.query(User).filter_by(email=data['email']).first():
            return jsonify({"error": "User already exists"}), 400

        # Hash the password before storing it
        hashed_password = generate_password_hash(data['password'])
        new_user = User(
            email=data['email'],
            password_hash=hashed_password,
            full_name=data.get('full_name')
        )
        session.add(new_user)
        session.commit()
        return jsonify({"message": "User registered successfully"}), 201

    except ValidationError as ve:
        session.rollback()
        return jsonify({"error": ve.messages}), 400
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    session = SessionLocal()
    try:
        json_data = request.get_json()
        # Validate input using LoginSchema
        schema = LoginSchema()
        data = schema.load(json_data)

        user = session.query(User).filter_by(email=data['email']).first()
        if not user or not check_password_hash(user.password_hash, data['password']):
            return jsonify({"error": "Invalid email or password"}), 401

        # Create a JWT access token (expires in 1 hour)
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
        return jsonify({"access_token": access_token}), 200

    except ValidationError as ve:
        return jsonify({"error": ve.messages}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()
