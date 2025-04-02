from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from app.core.config import settings
from app.core.monitoring import init_monitoring
from app.api.rpc import rpc_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="OpenMCP Server",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up monitoring
init_monitoring()
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Include RPC routes
app.include_router(rpc_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.MCP_HOST,
        port=settings.MCP_PORT,
        reload=settings.MCP_RELOAD,
    ) 