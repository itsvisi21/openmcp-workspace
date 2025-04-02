import pytest
from fastapi.testclient import TestClient
from app.schemas.context import ContextCreate, ContextResponse
from app.models.context import Context
from uuid import UUID

def test_create_context(client: TestClient):
    context_data = {
        "type": "test",
        "content": "Test content",
        "context_metadata": {"test": "value"}
    }
    response = client.post("/api/v1/contexts/", json=context_data)
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == context_data["type"]
    assert data["content"] == context_data["content"]
    assert data["context_metadata"] == context_data["context_metadata"]
    assert "id" in data
    assert UUID(data["id"])  # Verify it's a valid UUID

def test_list_contexts(client: TestClient):
    # First create a context
    context_data = {
        "type": "test",
        "content": "Test content",
        "context_metadata": {"test": "value"}
    }
    client.post("/api/v1/contexts/", json=context_data)
    
    # Then list contexts
    response = client.get("/api/v1/contexts/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["type"] == context_data["type"]

def test_get_context(client: TestClient):
    # First create a context
    context_data = {
        "type": "test",
        "content": "Test content",
        "context_metadata": {"test": "value"}
    }
    create_response = client.post("/api/v1/contexts/", json=context_data)
    context_id = create_response.json()["id"]
    
    # Then get the context
    response = client.get(f"/api/v1/contexts/{context_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == context_id
    assert data["type"] == context_data["type"]

def test_delete_context(client: TestClient):
    # First create a context
    context_data = {
        "type": "test",
        "content": "Test content",
        "context_metadata": {"test": "value"}
    }
    create_response = client.post("/api/v1/contexts/", json=context_data)
    context_id = create_response.json()["id"]
    
    # Then delete the context
    response = client.delete(f"/api/v1/contexts/{context_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Context deleted successfully"
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/contexts/{context_id}")
    assert get_response.status_code == 404 