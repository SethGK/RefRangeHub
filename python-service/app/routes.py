from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import ReferenceRange, Department
from app.database import SessionLocal
from app.schemas import ReferenceRangeSchema
from marshmallow import ValidationError

test_bp = Blueprint('test_bp', __name__)

@test_bp.route('/tests', methods=['POST'])
@jwt_required()
def create_test():
    session = SessionLocal()
    user_id = get_jwt_identity()
    
    try:
        json_data = request.get_json()
        schema = ReferenceRangeSchema()
        data = schema.load(json_data)
        
        new_test = ReferenceRange(
            test_name=data['test_name'],
            min_value=data['min_value'],
            max_value=data['max_value'],
            units=data['units'],
            department_id=data['department_id'],
            source_id=data.get('source_id'),
            study_id=data.get('study_id'),
            created_by=user_id
        )
        session.add(new_test)
        session.commit()
        return jsonify({"message": "Test created", "id": new_test.id}), 201
    except ValidationError as ve:
        session.rollback()
        return jsonify({"error": ve.messages}), 400
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@test_bp.route('/tests', methods=['GET'])
@jwt_required()
def get_user_tests():
    session = SessionLocal()
    user_id = get_jwt_identity()
    try:
        tests = session.query(ReferenceRange).filter_by(created_by=user_id).all()
        results = [{
            "id": t.id,
            "test_name": t.test_name,
            "min_value": t.min_value,
            "max_value": t.max_value,
            "units": t.units,
            "department_id": t.department_id,
            "source_id": t.source_id,
            "study_id": t.study_id,
            "created_at": t.created_at.isoformat()
        } for t in tests]
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@test_bp.route('/tests/<int:test_id>', methods=['PUT'])
@jwt_required()
def update_test(test_id):
    session = SessionLocal()
    user_id = get_jwt_identity()
    try:
        json_data = request.get_json()
        # Validate input data
        schema = ReferenceRangeSchema(partial=True)
        data = schema.load(json_data)
        
        test_item = session.query(ReferenceRange).filter_by(id=test_id, created_by=user_id).first()
        if not test_item:
            return jsonify({"error": "Test not found"}), 404

        for key, value in data.items():
            setattr(test_item, key, value)
        
        session.commit()
        return jsonify({"message": "Test updated"}), 200
    except ValidationError as ve:
        session.rollback()
        return jsonify({"error": ve.messages}), 400
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@test_bp.route('/tests/<int:test_id>', methods=['DELETE'])
@jwt_required()
def delete_test(test_id):
    session = SessionLocal()
    user_id = get_jwt_identity()
    try:
        test_item = session.query(ReferenceRange).filter_by(id=test_id, created_by=user_id).first()
        if not test_item:
            return jsonify({"error": "Test not found"}), 404
        
        session.delete(test_item)
        session.commit()
        return jsonify({"message": "Test deleted"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@test_bp.route('/departments/<int:dept_id>/tests', methods=['GET'])
@jwt_required()
def get_tests_by_department(dept_id):
    session = SessionLocal()
    user_id = get_jwt_identity()
    try:
        tests = session.query(ReferenceRange).filter_by(department_id=dept_id, created_by=user_id).all()
        results = [{
            "id": t.id,
            "test_name": t.test_name,
            "min_value": t.min_value,
            "max_value": t.max_value,
            "units": t.units,
            "department_id": t.department_id,
            "source_id": t.source_id,
            "study_id": t.study_id,
            "created_at": t.created_at.isoformat()
        } for t in tests]
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@test_bp.route('/departments', methods=['POST'])
@jwt_required()
def create_department():
    session = SessionLocal()
    user_id = get_jwt_identity()
    
    try:
        json_data = request.get_json()
        department_name = json_data.get("name")
        department_description = json_data.get("description", "")
        
        if not department_name:
            return jsonify({"error": "Department name is required"}), 400
        
        new_department = Department(
            name=department_name,
            description=department_description
        )
        
        session.add(new_department)
        session.commit()
        
        return jsonify({"message": "Department created", "id": new_department.id}), 201
    
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

