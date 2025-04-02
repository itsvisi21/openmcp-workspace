import hashlib
import json
from typing import Optional
import boto3
from botocore.exceptions import ClientError

from app.core.config import settings

class StorageService:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )
        self.bucket = settings.AWS_BUCKET_NAME

    def _compute_hash(self, content: str) -> str:
        """Compute SHA-256 hash of content."""
        return hashlib.sha256(content.encode()).hexdigest()

    async def store(self, content: str) -> str:
        """Store content in S3 and return content hash."""
        content_hash = self._compute_hash(content)
        try:
            self.s3.put_object(
                Bucket=self.bucket,
                Key=f"context/{content_hash}/content",
                Body=content.encode(),
            )
            return content_hash
        except ClientError as e:
            raise Exception(f"Failed to store content: {str(e)}")

    async def retrieve(self, content_hash: str) -> str:
        """Retrieve content from S3 by hash."""
        try:
            response = self.s3.get_object(
                Bucket=self.bucket,
                Key=f"context/{content_hash}/content",
            )
            return response['Body'].read().decode()
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                raise Exception(f"Content not found: {content_hash}")
            raise Exception(f"Failed to retrieve content: {str(e)}")

    async def delete(self, content_hash: str) -> None:
        """Delete content from S3 by hash."""
        try:
            self.s3.delete_object(
                Bucket=self.bucket,
                Key=f"context/{content_hash}/content",
            )
        except ClientError as e:
            raise Exception(f"Failed to delete content: {str(e)}")

    async def store_metadata(self, content_hash: str, metadata: dict) -> None:
        """Store metadata in S3."""
        try:
            self.s3.put_object(
                Bucket=self.bucket,
                Key=f"context/{content_hash}/metadata",
                Body=json.dumps(metadata).encode(),
            )
        except ClientError as e:
            raise Exception(f"Failed to store metadata: {str(e)}")

    async def retrieve_metadata(self, content_hash: str) -> Optional[dict]:
        """Retrieve metadata from S3."""
        try:
            response = self.s3.get_object(
                Bucket=self.bucket,
                Key=f"context/{content_hash}/metadata",
            )
            return json.loads(response['Body'].read().decode())
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                return None
            raise Exception(f"Failed to retrieve metadata: {str(e)}")

    async def delete_metadata(self, content_hash: str) -> None:
        """Delete metadata from S3."""
        try:
            self.s3.delete_object(
                Bucket=self.bucket,
                Key=f"context/{content_hash}/metadata",
            )
        except ClientError as e:
            raise Exception(f"Failed to delete metadata: {str(e)}") 