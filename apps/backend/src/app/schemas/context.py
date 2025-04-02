from datetime import datetime
from typing import Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field

class ContextBase(BaseModel):
    type: str = Field(..., description="Type of context (code, documentation, conversation, other)")
    context_metadata: Dict[str, Any] | None = None

class ContextCreate(ContextBase):
    content: str = Field(..., description="Content to be stored")

class ContextResponse(ContextBase):
    id: UUID
    content: str
    content_hash: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 