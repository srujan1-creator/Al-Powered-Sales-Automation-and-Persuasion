from fastapi.testclient import TestClient
from main import app
from database import Base, engine
from config import settings

# Create tables
Base.metadata.create_all(bind=engine)

client = TestClient(app)
HEADERS = {"X-API-Key": settings.backend_api_key}

def test_unauthorized_access():
    response = client.post("/api/context", json={})
    assert response.status_code == 403

def test_create_context():
    response = client.post(
        "/api/context",
        headers=HEADERS,
        json={
            "company_size": "50-100",
            "industry": "Software",
            "pain_points": "Slow lead qualification"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["status"] == "active"
    assert len(data["messages"]) > 0
    assert data["messages"][0]["sender"] == "ai"

def test_send_message():
    # First create a context
    context_response = client.post(
        "/api/context",
        headers=HEADERS,
        json={"company_size": "1-10", "industry": "Retail", "pain_points": "High costs"}
    )
    conversation_id = context_response.json()["id"]

    # Send a message
    response = client.post(
        "/api/chat",
        headers=HEADERS,
        json={
            "conversation_id": conversation_id,
            "message": "We need to reduce our server costs immediately."
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["messages"]) >= 3 # Intro, user message, AI response
    assert data["messages"][-2]["sender"] == "user"
    assert data["messages"][-1]["sender"] == "ai"

def test_get_conversation():
    # First create a context
    context_response = client.post(
        "/api/context",
        headers=HEADERS,
        json={"company_size": "1000+", "industry": "Finance", "pain_points": "Compliance overhead"}
    )
    conversation_id = context_response.json()["id"]

    # Get conversation
    response = client.get(f"/api/conversation/{conversation_id}", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == conversation_id
