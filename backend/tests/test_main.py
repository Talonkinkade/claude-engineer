from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Educational Content Generator API"}

def test_create_teks_standard():
    response = client.post(
        "/teks_standards/",
        json={"standard_code": "TEST.1", "description": "Test TEKS standard"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["standard_code"] == "TEST.1"
    assert data["description"] == "Test TEKS standard"
    assert "id" in data

def test_generate_question():
    # First, create a TEKS standard
    teks_response = client.post(
        "/teks_standards/",
        json={"standard_code": "TEST.2", "description": "Another test TEKS standard"}
    )
    teks_id = teks_response.json()["id"]

    # Now, generate a question based on this TEKS standard
    response = client.post(
        "/generate_question/",
        json={
            "teks_standard_id": teks_id,
            "difficulty": 3,
            "question_type": "multiple_choice"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "question_text" in data
    assert data["question_type"] == "multiple_choice"
    assert data["difficulty"] == 3
    assert data["teks_standard_id"] == teks_id