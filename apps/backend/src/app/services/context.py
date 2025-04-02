from datetime import datetime
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.context import Context
from app.schemas.context import ContextCreate, ContextResponse
from app.services.storage import StorageService

class ContextService:
    def __init__(self, db: Session, storage_service: StorageService):
        self.db = db
        self.storage_service = storage_service

    async def create_context(self, context: ContextCreate) -> ContextResponse:
        # Store content in S3
        content_hash = await self.storage_service.store(context.content)
        
        # Create database record
        db_context = Context(
            type=context.type,
            content=context.content,
            content_hash=content_hash,
            context_metadata=context.context_metadata
        )
        
        self.db.add(db_context)
        self.db.commit()
        self.db.refresh(db_context)
        
        return ContextResponse.model_validate(db_context)

    def get_contexts(self) -> List[ContextResponse]:
        contexts = self.db.query(Context).all()
        return [ContextResponse.model_validate(context) for context in contexts]

    def get_context(self, context_id: UUID) -> Optional[ContextResponse]:
        context = self.db.query(Context).filter(Context.id == context_id).first()
        if context:
            return ContextResponse.model_validate(context)
        return None

    async def delete_context(self, context_id: UUID) -> bool:
        context = self.db.query(Context).filter(Context.id == context_id).first()
        if context:
            # Delete content from S3
            await self.storage_service.delete(context.content_hash)
            
            # Delete database record
            self.db.delete(context)
            self.db.commit()
            return True
        return False 