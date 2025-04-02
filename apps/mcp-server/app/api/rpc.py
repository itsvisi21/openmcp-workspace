from typing import Dict, Any, Union
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class RPCRequest(BaseModel):
    """JSON-RPC request model."""
    jsonrpc: str = "2.0"
    method: str
    params: Dict[str, Any] = {}
    id: str

class RPCResponse(BaseModel):
    """JSON-RPC response model."""
    jsonrpc: str = "2.0"
    result: Any
    id: str

class RPCError(BaseModel):
    """JSON-RPC error model."""
    jsonrpc: str = "2.0"
    error: Dict[str, Any]
    id: str

@router.post("/", response_model=Union[RPCResponse, RPCError])
async def handle_rpc(request: RPCRequest) -> Union[RPCResponse, RPCError]:
    """Handle JSON-RPC requests."""
    try:
        if request.method == "mcp_commitContext":
            # TODO: Implement context commit
            return RPCResponse(
                result={"content_hash": "test_hash"},
                id=request.id
            )

        elif request.method == "mcp_getContext":
            # TODO: Implement context retrieval
            return RPCResponse(
                result={
                    "content": "Test content",
                    "type": "test",
                    "metadata": {}
                },
                id=request.id
            )

        elif request.method == "mcp_processContext":
            # TODO: Implement context processing
            return RPCResponse(
                result={
                    "response": "Processed content",
                    "metadata": {}
                },
                id=request.id
            )

        else:
            return RPCError(
                error={
                    "code": -32601,
                    "message": f"Method not found: {request.method}",
                },
                id=request.id
            )

    except Exception as e:
        return RPCError(
            error={
                "code": -32603,
                "message": "Internal error",
                "data": str(e),
            },
            id=request.id
        ) 