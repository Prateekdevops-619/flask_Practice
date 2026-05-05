import sys
import os
from unittest.mock import MagicMock, patch
import pytest

# Mock conflicting modules BEFORE importing app to bypass bson/pymongo conflicts
sys.modules['pymongo'] = MagicMock()
sys.modules['flask_pymongo'] = MagicMock()
sys.modules['bson'] = MagicMock()
sys.modules['bson.objectid'] = MagicMock()

os.environ.setdefault("MONGO_URI", "mongodb://localhost:27017/test_students")
os.environ.setdefault("SECRET_KEY", "test-secret-key")

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_page(client):
    with patch("app.mongo") as mock_mongo:
        mock_mongo.db.students.find.return_value = []
        response = client.get("/")
        assert response.status_code == 200


def test_add_student_get(client):
    response = client.get("/add")
    assert response.status_code == 200


def test_add_student_post(client):
    with patch("app.mongo") as mock_mongo:
        mock_mongo.db.students.insert_one.return_value = MagicMock()
        response = client.post("/add", data={
            "name": "John Doe",
            "email": "john@example.com",
            "course": "Python"
        }, follow_redirects=False)
        assert response.status_code == 302
        mock_mongo.db.students.insert_one.assert_called_once()


def test_update_student_get(client):
    fake_id = "507f1f77bcf86cd799439011"
    with patch("app.mongo") as mock_mongo:
        mock_mongo.db.students.find_one.return_value = {
            "_id": fake_id,
            "name": "Jane",
            "email": "jane@example.com",
            "course": "Flask"
        }
        response = client.get(f"/update/{fake_id}")
        assert response.status_code == 200


def test_update_student_post(client):
    fake_id = "507f1f77bcf86cd799439011"
    with patch("app.mongo") as mock_mongo:
        mock_mongo.db.students.update_one.return_value = MagicMock()
        response = client.post(f"/update/{fake_id}", data={
            "name": "Jane Updated",
            "email": "jane2@example.com",
            "course": "Django"
        }, follow_redirects=False)
        assert response.status_code == 302
        mock_mongo.db.students.update_one.assert_called_once()


def test_delete_student(client):
    fake_id = "507f1f77bcf86cd799439011"
    with patch("app.mongo") as mock_mongo:
        mock_mongo.db.students.delete_one.return_value = MagicMock()
        response = client.get(f"/delete/{fake_id}", follow_redirects=False)
        assert response.status_code == 302
        mock_mongo.db.students.delete_one.assert_called_once()
