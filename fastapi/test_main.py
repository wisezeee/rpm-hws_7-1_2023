from fastapi.testclient import TestClient
from main import app
from config import OK, NOT_FOUND

client = TestClient(app)


def test_read_route():
    response = client.get("/")
    assert response.status_code == OK


def test_read_media_api():
    response = client.get("/media_api")
    assert response.status_code == OK


def test_read_media_api_ind():
    response = client.get("/media_api/1")
    assert response.status_code == OK


def test_wrong_url():
    response = client.get("/med_api")
    assert response.status_code == NOT_FOUND
