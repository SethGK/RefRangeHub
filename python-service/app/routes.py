from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import ReferenceRange
from app.database import SessionLocal

test_bp = Blueprint('test_bp', __name__)

@test_bp.route('/tests', methods=['POST'])
@jwt_required()
def create_test():
    session = SessionLocal()
    user_id = get_jwt_identity()
    try:
        data = request.get_json()
        new_test = ReferenceRange(
            test_name=data['test_name'],
            min_value=data.get('min_value'),
            max_value=data.get('max_value'),
            units=data.get('units'),
            department_id=data['department_id'],
            source_id=data.get('source_id'),
            study_id=data.get('study_id'),
            created_by=user_id
        )
        session.add(new_test)
        session.commit()
        return jsonify({"message": "Test created", "id": new_test.id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

# Retrieve all tests
@test_bp.route('/tests', methods=['GET'])
def get_tests():
    session = SessionLocal()
    try:
        # Optional query parameter to filter tests by department
        department_id = request.args.get('department_id')
        if department_id:
            tests = session.query(ReferenceRange).filter_by(department_id=department_id).all()
        else:
            tests = session.query(ReferenceRange).all()
        
        results = []
        for t in tests:
            results.append({
                "id": t.id,
                "test_name": t.test_name,
                "min_value": t.min_value,
                "max_value": t.max_value,
                "units": t.units,
                "department_id": t.department_id,
                "source_id": t.source_id,
                "study_id": t.study_id,
                "created_by": t.created_by,
                "created_at": t.created_at.isoformat()
            })
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

# Update an existing test
@test_bp.route('/tests/<int:test_id>', methods=['PUT'])
def update_test(test_id):
    session = SessionLocal()
    try:
        data = request.get_json()
        test_item = session.query(ReferenceRange).filter_by(id=test_id).first()
        if not test_item:
            return jsonify({"error": "Test not found"}), 404

        # Update fields if provided
        test_item.test_name = data.get('test_name', test_item.test_name)
        test_item.min_value = data.get('min_value', test_item.min_value)
        test_item.max_value = data.get('max_value', test_item.max_value)
        test_item.units = data.get('units', test_item.units)
        test_item.department_id = data.get('department_id', test_item.department_id)
        test_item.source_id = data.get('source_id', test_item.source_id)
        test_item.study_id = data.get('study_id', test_item.study_id)

        session.commit()
        return jsonify({"message": "Test updated"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

# Delete a test
@test_bp.route('/tests/<int:test_id>', methods=['DELETE'])
def delete_test(test_id):
    session = SessionLocal()
    try:
        test_item = session.query(ReferenceRange).filter_by(id=test_id).first()
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

# Retrieve tests organized by department
@test_bp.route('/departments/<int:dept_id>/tests', methods=['GET'])
def get_tests_by_department(dept_id):
    session = SessionLocal()
    try:
        tests = session.query(ReferenceRange).filter_by(department_id=dept_id).all()
        results = []
        for t in tests:
            results.append({
                "id": t.id,
                "test_name": t.test_name,
                "min_value": t.min_value,
                "max_value": t.max_value,
                "units": t.units,
                "department_id": t.department_id,
                "source_id": t.source_id,
                "study_id": t.study_id,
                "created_by": t.created_by,
                "created_at": t.created_at.isoformat()
            })
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()
