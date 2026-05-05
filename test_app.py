import pytest
import os
from unittest.mock import patch, MagicMock
from bson.objectid import ObjectId

os.environ.setdefault("MONGO_URI", "mongodb://localhost:27017/test_students")
os.environ.setdefault("SECRET_KEY", "test-secret-key")

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@patch("app.mongo")
def test_index_page(mock_mongo, client):
    mock_mongo.db.students.find.return_value = []
    response = client.get("/")
    assert response.status_code == 200


@patch("app.mongo")
def test_add_student_get(mock_mongo, client):
    response = client.get("/add")
    assert response.status_code == 200


@patch("app.mongo")
def test_add_student_post(mock_mongo, client):
    mock_mongo.db.students.insert_one.return_value = MagicMock()
    response = client.post("/add", data={
        "name": "John Doe",
        "email": "john@example.com",
        "course": "Python"
    }, follow_redirects=False)
    assert response.status_code == 302
    mock_mongo.db.students.insert_one.assert_called_once()


@patch("app.mongo")
def test_update_student_get(mock_mongo, client):
    fake_id = str(ObjectId())
    mock_mongo.db.students.find_one.return_value = {
        "_id": ObjectId(fake_id),
        "name": "Jane",
        "email": "jane@example.com",
        "course": "Flask"
    }
    response = client.get(f"/update/{fake_id}")
    assert response.status_code == 200


@patch("app.mongo")
def test_update_student_post(mock_mongo, client):
    fake_id = str(ObjectId())
    mock_mongo.db.students.update_one.return_value = MagicMock()
    response = client.post(f"/update/{fake_id}", data={
        "name": "Jane Updated",
        "email": "jane2@example.com",
        "course": "Django"
    }, follow_redirects=False)
    assert response.status_code == 302
    mock_mongo.db.students.update_one.assert_called_once()


@patch("app.mongo")
def test_delete_student(mock_mongo, client):
    fake_id = str(ObjectId())
    mock_mongo.db.students.delete_one.return_value = MagicMock()
    response = client.get(f"/delete/{fake_id}", follow_redirects=False)
    assert response.status_code == 302
    mock_mongo.db.students.delete_one.assert_called_once()
