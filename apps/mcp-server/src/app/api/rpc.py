from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Any, Optional, Dict
from app.services.storage import StorageService
from app.services.llm import LLMService

router = APIRouter()

class RPCRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: Optional[dict[str, Any]] = None
    id: Optional[str | int] = None

class RPCResponse(BaseModel):
    jsonrpc: str = "2.0"
    result: Any
    id: Optional[str | int] = None

class RPCError(BaseModel):
    jsonrpc: str = "2.0"
    error: Dict[str, Any]
    id: Optional[str | int] = None

def get_storage_service() -> StorageService:
    return StorageService()

def get_llm_service() -> LLMService:
    return LLMService()

@router.post("/rpc")
async def handle_rpc(
    request: RPCRequest,
    storage_service: StorageService = Depends(get_storage_service),
    llm_service: LLMService = Depends(get_llm_service)
) -> RPCResponse | RPCError:
    try:
        if request.method == "commit_context":
            result = await storage_service.commit_context(request.params or {})
        elif request.method == "get_context":
            result = await storage_service.get_context(request.params or {})
        elif request.method == "process_context":
            result = await llm_service.process_context(request.params or {})
        else:
            return RPCError(
                error={
                    "code": -32601,
                    "message": f"Method '{request.method}' not found",
                    "data": None
                },
                id=request.id
            )
        
        return RPCResponse(result=result, id=request.id)
    except Exception as e:
        return RPCError(
            error={
                "code": -32000,
                "message": str(e),
                "data": None
            },
            id=request.id
        ) 