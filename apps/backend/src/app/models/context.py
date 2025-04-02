from datetime import datetime
from typing import Dict, Any
from sqlalchemy import Column, String, DateTime, JSON
import uuid

from app.db.base import Base
from app.db.types import UUID

class Context(Base):
    __tablename__ = "contexts"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    type = Column(String, nullable=False)
    content = Column(String, nullable=False)
    content_hash = Column(String, nullable=False)
    context_metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "content_hash": self.content_hash,
            "type": self.type,
            "metadata": self.context_metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        } 