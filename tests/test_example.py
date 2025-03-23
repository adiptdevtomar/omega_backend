import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_example_endpoint():
    response = client.get("/api/v1/example")
    assert response.status_code == 200
    assert "data" in response.json()  # Adjust based on actual response structure

def test_example_service():
    # Assuming there's a service function to test
    from app.services.example_service import example_function
    result = example_function()
    assert result is not None  # Replace with actual expected result check