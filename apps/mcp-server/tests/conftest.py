import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.rpc import RPCRequest

# Set the environment file path for tests
os.environ["ENV_FILE"] = os.path.join(os.path.dirname(__file__), ".env")

@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)

@pytest.fixture
def mock_storage_service(mocker):
    """Mock storage service for testing."""
    mock = mocker.Mock()
    mock.commit_context.return_value = {"content_hash": "test_hash"}
    mock.get_context.return_value = {
        "content": "Test content",
        "type": "test",
        "metadata": {}
    }
    return mock

@pytest.fixture
def mock_llm_service(mocker):
    """Mock LLM service for testing."""
    mock = mocker.Mock()
    mock.process_context.return_value = {
        "response": "Processed content",
        "metadata": {}
    }
    return mock 