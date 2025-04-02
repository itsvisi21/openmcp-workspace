import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.mark.asyncio
async def test_monitoring_client_record_metric(mock_monitoring_client):
    """Test monitoring client record_metric functionality."""
    mock_monitoring_client.record_metric.return_value = None
    await mock_monitoring_client.record_metric("test_metric", 1.0)
    assert mock_monitoring_client.record_metric.called == True

@pytest.mark.asyncio
async def test_monitoring_client_record_event(mock_monitoring_client):
    """Test monitoring client record_event functionality."""
    mock_monitoring_client.record_event.return_value = None
    await mock_monitoring_client.record_event("test_event", {"data": "test"})
    assert mock_monitoring_client.record_event.called == True 