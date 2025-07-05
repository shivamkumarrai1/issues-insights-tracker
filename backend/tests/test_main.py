from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/auth/health")  # or your own health route
    assert response.status_code == 200
