import pytest
import json
from datetime import datetime, timedelta

from flask_jwt_extended import create_access_token
from app.main import create_app
from app.database import SessionLocal, Base, engine
from app.models import User, ReferenceRange, Department, Source, Study

# -----------------------------
# Fixtures
# -----------------------------

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

# This fixture will run for every test to create and drop all tables.
@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_user():
    session = SessionLocal()
    user = User(
        email='test@example.com',
        password_hash='hashed_password',
        full_name='Test User',
        created_at=datetime.utcnow()
    )
    session.add(user)
    session.commit()
    user_id = user.id
    session.close()
    return user_id

@pytest.fixture
def test_department():
    session = SessionLocal()
    dept = Department(name="Chemistry", description="Chemistry Department")
    session.add(dept)
    session.commit()
    dept_id = dept.id
    session.close()
    return dept_id

@pytest.fixture
def test_source():
    session = SessionLocal()
    src = Source(name="Test Source", url="http://example.com", source_type="Study")
    session.add(src)
    session.commit()
    src_id = src.id
    session.close()
    return src_id

@pytest.fixture
def test_study():
    session = SessionLocal()
    study = Study(title="Test Study", authors="Author", publication_date=datetime.utcnow())
    session.add(study)
    session.commit()
    study_id = study.id
    session.close()
    return study_id

def get_token(app, identity):
    with app.app_context():
        token = create_access_token(identity=identity, expires_delta=timedelta(hours=1))
        return token

# -----------------------------
# Test Cases
# -----------------------------

def test_create_test(client, app, test_user, test_department, test_source, test_study):
    token = get_token(app, identity=test_user)
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = {
        "test_name": "Glucose",
        "min_value": 70.0,
        "max_value": 100.0,
        "units": "mg/dL",
        "department_id": test_department,
        "source_id": test_source,
        "study_id": test_study
    }
    response = client.post('/api/tests', headers=headers, data=json.dumps(payload))
    # Expecting 201 Created
    assert response.status_code == 201, response.get_data(as_text=True)
    data = response.get_json()
    assert "id" in data
    assert data["message"] == "Test created"

def test_get_user_tests(client, app, test_user, test_department):
    token = get_token(app, identity=test_user)
    headers = {
        'Authorization': f'Bearer {token}',
    }
    session = SessionLocal()
    test_record = ReferenceRange(
        test_name="Hemoglobin",
        min_value=12.0,
        max_value=16.0,
        units="g/dL",
        department_id=test_department,
        created_by=test_user,
        created_at=datetime.utcnow()
    )
    session.add(test_record)
    session.commit()
    session.close()

    response = client.get('/api/tests', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_update_test(client, app, test_user, test_department):
    token = get_token(app, identity=test_user)
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    session = SessionLocal()
    test_record = ReferenceRange(
        test_name="Cholesterol",
        min_value=150.0,
        max_value=200.0,
        units="mg/dL",
        department_id=test_department,
        created_by=test_user,
        created_at=datetime.utcnow()
    )
    session.add(test_record)
    session.commit()
    test_id = test_record.id
    session.close()

    update_payload = {
        "test_name": "Total Cholesterol"
    }
    response = client.put(f'/api/tests/{test_id}', headers=headers, data=json.dumps(update_payload))
    assert response.status_code == 200, response.get_data(as_text=True)
    data = response.get_json()
    assert data["message"] == "Test updated"

def test_delete_test(client, app, test_user, test_department):
    token = get_token(app, identity=test_user)
    headers = {
        'Authorization': f'Bearer {token}'
    }
    # Create a test record to delete
    session = SessionLocal()
    test_record = ReferenceRange(
        test_name="Triglycerides",
        min_value=50.0,
        max_value=150.0,
        units="mg/dL",
        department_id=test_department,
        created_by=test_user,
        created_at=datetime.utcnow()
    )
    session.add(test_record)
    session.commit()
    test_id = test_record.id
    session.close()

    response = client.delete(f'/api/tests/{test_id}', headers=headers)
    assert response.status_code == 200, response.get_data(as_text=True)
    data = response.get_json()
    assert data["message"] == "Test deleted"

def test_get_tests_by_department(client, app, test_user, test_department):
    token = get_token(app, identity=test_user)
    headers = {
        'Authorization': f'Bearer {token}'
    }
    # Create two test records in the same department
    session = SessionLocal()
    test1 = ReferenceRange(
        test_name="Test A",
        min_value=1.0,
        max_value=2.0,
        units="units",
        department_id=test_department,
        created_by=test_user,
        created_at=datetime.utcnow()
    )
    test2 = ReferenceRange(
        test_name="Test B",
        min_value=2.0,
        max_value=3.0,
        units="units",
        department_id=test_department,
        created_by=test_user,
        created_at=datetime.utcnow()
    )
    session.add_all([test1, test2])
    session.commit()
    session.close()

    response = client.get(f'/api/departments/{test_department}/tests', headers=headers)
    assert response.status_code == 200, response.get_data(as_text=True)
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2
