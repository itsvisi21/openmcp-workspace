import pytest
from fastapi.testclient import TestClient
from app.api.rpc import RPCRequest

def test_commit_context(client: TestClient, mock_storage_service):
    """Test commit_context RPC method."""
    rpc_request = {
        "jsonrpc": "2.0",
        "method": "commit_context",
        "params": {
            "content": "Test content",
            "type": "test"
        },
        "id": "1"
    }

    response = client.post("/api/v1/rpc", json=rpc_request)
    assert response.status_code == 200
    data = response.json()
    assert data["jsonrpc"] == "2.0"
    assert data["id"] == "1"
    assert "content_hash" in data["result"]

def test_get_context(client: TestClient, mock_storage_service):
    """Test get_context RPC method."""
    rpc_request = {
        "jsonrpc": "2.0",
        "method": "get_context",
        "params": {
            "content_hash": "test_hash"
        },
        "id": "1"
    }

    response = client.post("/api/v1/rpc", json=rpc_request)
    assert response.status_code == 200
    data = response.json()
    assert data["jsonrpc"] == "2.0"
    assert data["id"] == "1"
    assert "content" in data["result"]
    assert "type" in data["result"]

def test_process_context(client: TestClient, mock_llm_service):
    """Test process_context RPC method."""
    rpc_request = {
        "jsonrpc": "2.0",
        "method": "process_context",
        "params": {
            "content": "Test content",
            "type": "test"
        },
        "id": "1"
    }

    response = client.post("/api/v1/rpc", json=rpc_request)
    assert response.status_code == 200
    data = response.json()
    assert data["jsonrpc"] == "2.0"
    assert data["id"] == "1"
    assert "response" in data["result"]
    assert "metadata" in data["result"]

def test_invalid_method(client: TestClient):
    """Test RPC request with invalid method."""
    rpc_request = {
        "jsonrpc": "2.0",
        "method": "invalid_method",
        "params": {},
        "id": "1"
    }

    response = client.post("/api/v1/rpc", json=rpc_request)
    assert response.status_code == 200
    data = response.json()
    assert data["jsonrpc"] == "2.0"
    assert data["id"] == "1"
    assert "error" in data
    assert data["error"]["code"] == -32601
    assert "Method 'invalid_method' not found" in data["error"]["message"]

def test_rpc_endpoint(client: TestClient):
    """Test the RPC endpoint."""
    request = RPCRequest(
        method="test",
        params={},
        id="1"
    )
    response = client.post("/api/v1/rpc", json=request.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert data["jsonrpc"] == "2.0"
    assert data["id"] == "1"
    assert "error" in data
    assert data["error"]["code"] == -32601
    assert "Method 'test' not found" in data["error"]["message"] 