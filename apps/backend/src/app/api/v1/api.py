from fastapi import APIRouter

from app.api.v1.endpoints import context

api_router = APIRouter()
api_router.include_router(context.router, prefix="/contexts", tags=["contexts"]) 