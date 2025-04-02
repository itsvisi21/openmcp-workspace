import os
import pytest
from unittest.mock import AsyncMock, MagicMock

# Set test environment file
os.environ["ENV_FILE"] = os.path.join(os.path.dirname(__file__), ".env")

@pytest.fixture
def mock_aws_client():
    """Mock AWS client for testing."""
    mock_client = MagicMock()
    mock_client.upload_file = AsyncMock()
    mock_client.download_file = AsyncMock()
    mock_client.delete_object = AsyncMock()
    mock_client.head_object = AsyncMock()
    return mock_client

@pytest.fixture
def mock_llm_client():
    """Mock LLM client for testing."""
    mock_client = MagicMock()
    mock_client.generate = AsyncMock()
    mock_client.embed = AsyncMock()
    return mock_client

@pytest.fixture
def mock_monitoring_client():
    """Mock monitoring client for testing."""
    mock_client = MagicMock()
    mock_client.record_metric = AsyncMock()
    mock_client.record_event = AsyncMock()
    return mock_client

@pytest.fixture
def test_context():
    """Test context data."""
    return {
        "content": "Test content",
        "type": "test",
        "metadata": {
            "source": "test",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    }

@pytest.fixture
def test_response():
    """Test response data."""
    return {
        "response": "Test response",
        "metadata": {
            "model": "test-model",
            "tokens": 10,
            "latency": 0.1
        }
    } 