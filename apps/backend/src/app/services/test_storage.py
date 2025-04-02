import hashlib
import json
import os
from pathlib import Path
from typing import Optional

class TestStorageService:
    def __init__(self):
        self.storage_dir = Path("test_storage")
        self.storage_dir.mkdir(exist_ok=True)

    def _compute_hash(self, content: str) -> str:
        """Compute SHA-256 hash of content."""
        return hashlib.sha256(content.encode()).hexdigest()

    def _get_context_dir(self, content_hash: str) -> Path:
        """Get the directory for a specific context."""
        return self.storage_dir / "context" / content_hash

    async def store(self, content: str) -> str:
        """Store content in local filesystem and return content hash."""
        content_hash = self._compute_hash(content)
        context_dir = self._get_context_dir(content_hash)
        context_dir.mkdir(parents=True, exist_ok=True)
        
        content_file = context_dir / "content"
        content_file.write_text(content)
        return content_hash

    async def retrieve(self, content_hash: str) -> str:
        """Retrieve content from local filesystem by hash."""
        content_file = self._get_context_dir(content_hash) / "content"
        if not content_file.exists():
            raise Exception(f"Content not found: {content_hash}")
        return content_file.read_text()

    async def delete(self, content_hash: str) -> None:
        """Delete content from local filesystem by hash."""
        context_dir = self._get_context_dir(content_hash)
        if context_dir.exists():
            for file in context_dir.glob("*"):
                file.unlink()
            context_dir.rmdir()

    async def store_metadata(self, content_hash: str, metadata: dict) -> None:
        """Store metadata in local filesystem."""
        context_dir = self._get_context_dir(content_hash)
        context_dir.mkdir(parents=True, exist_ok=True)
        metadata_file = context_dir / "metadata"
        metadata_file.write_text(json.dumps(metadata))

    async def retrieve_metadata(self, content_hash: str) -> Optional[dict]:
        """Retrieve metadata from local filesystem."""
        metadata_file = self._get_context_dir(content_hash) / "metadata"
        if not metadata_file.exists():
            return None
        return json.loads(metadata_file.read_text())

    async def delete_metadata(self, content_hash: str) -> None:
        """Delete metadata from local filesystem."""
        metadata_file = self._get_context_dir(content_hash) / "metadata"
        if metadata_file.exists():
            metadata_file.unlink()

    def cleanup(self):
        """Clean up all test storage."""
        if self.storage_dir.exists():
            for file in self.storage_dir.glob("**/*"):
                if file.is_file():
                    file.unlink()
            for dir in reversed(list(self.storage_dir.glob("**/*"))):
                if dir.is_dir():
                    dir.rmdir()
            self.storage_dir.rmdir() 