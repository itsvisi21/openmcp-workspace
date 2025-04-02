from typing import Optional
import boto3
from pydantic import BaseModel

class S3Client:
    def __init__(self, bucket_name: Optional[str] = None):
        self.bucket_name = bucket_name
        self.client = boto3.client('s3')

    async def upload_file(self, file_path: str, bucket: Optional[str] = None, key: Optional[str] = None) -> str:
        """Upload a file to S3."""
        bucket = bucket or self.bucket_name
        if not bucket:
            raise ValueError("Bucket name must be provided")
        
        key = key or file_path.split('/')[-1]
        await self.client.upload_file(file_path, bucket, key)
        return key

    async def download_file(self, key: str, bucket: Optional[str] = None, destination: Optional[str] = None) -> str:
        """Download a file from S3."""
        bucket = bucket or self.bucket_name
        if not bucket:
            raise ValueError("Bucket name must be provided")
        
        destination = destination or key.split('/')[-1]
        await self.client.download_file(bucket, key, destination)
        return destination

    async def delete_object(self, key: str, bucket: Optional[str] = None) -> bool:
        """Delete an object from S3."""
        bucket = bucket or self.bucket_name
        if not bucket:
            raise ValueError("Bucket name must be provided")
        
        await self.client.delete_object(Bucket=bucket, Key=key)
        return True 