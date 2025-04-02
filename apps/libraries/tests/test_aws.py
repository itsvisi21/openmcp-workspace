import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.mark.asyncio
async def test_s3_client_upload(mock_aws_client):
    """Test S3 client upload functionality."""
    mock_aws_client.upload_file.return_value = "test_hash"
    result = await mock_aws_client.upload_file("test.txt")
    assert result == "test_hash"
    assert mock_aws_client.upload_file.called == True
    
@pytest.mark.asyncio
async def test_s3_client_download(mock_aws_client):
    """Test S3 client download functionality."""
    mock_aws_client.download_file.return_value = "test_content"
    result = await mock_aws_client.download_file("test.txt")
    assert result == "test_content"
    assert mock_aws_client.download_file.called == True

@pytest.mark.asyncio
async def test_s3_client_delete(mock_aws_client):
    """Test S3 client delete functionality."""
    mock_aws_client.delete_object.return_value = True
    result = await mock_aws_client.delete_object("test.txt")
    assert result == True
    assert mock_aws_client.delete_object.called == True 