from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.monitoring import track_context_commit, track_context_retrieval
from app.db.session import get_db
from app.models.context import Context
from app.schemas.context import ContextCreate, ContextResponse
from app.services.storage import StorageService
from app.services.context import ContextService

router = APIRouter()

def get_context_service(db: Session = Depends(get_db)) -> ContextService:
    storage_service = StorageService()
    return ContextService(db, storage_service)

@router.post("/", response_model=ContextResponse)
async def create_context(
    context: ContextCreate,
    service: ContextService = Depends(get_context_service)
):
    return await service.create_context(context)

@router.get("/", response_model=List[ContextResponse])
def list_contexts(
    service: ContextService = Depends(get_context_service)
):
    return service.get_contexts()

@router.get("/{context_id}", response_model=ContextResponse)
def get_context(
    context_id: UUID,
    service: ContextService = Depends(get_context_service)
):
    context = service.get_context(context_id)
    if not context:
        raise HTTPException(status_code=404, detail="Context not found")
    return context

@router.delete("/{context_id}")
async def delete_context(
    context_id: UUID,
    service: ContextService = Depends(get_context_service)
):
    success = await service.delete_context(context_id)
    if not success:
        raise HTTPException(status_code=404, detail="Context not found")
    return {"message": "Context deleted successfully"} 