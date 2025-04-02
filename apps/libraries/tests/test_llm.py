import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.mark.asyncio
async def test_llm_client_generate(mock_llm_client, test_response):
    """Test LLM client generate functionality."""
    mock_llm_client.generate.return_value = test_response
    result = await mock_llm_client.generate("test prompt")
    assert result == test_response
    assert mock_llm_client.generate.called == True

@pytest.mark.asyncio
async def test_llm_client_embed(mock_llm_client):
    """Test LLM client embed functionality."""
    mock_llm_client.embed.return_value = [0.1, 0.2, 0.3]
    result = await mock_llm_client.embed("test text")
    assert result == [0.1, 0.2, 0.3]
    assert mock_llm_client.embed.called == True 