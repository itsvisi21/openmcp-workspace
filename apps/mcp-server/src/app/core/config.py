from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
import os

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "OpenMCP MCP Server"
    VERSION: str = "0.1.0"

    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]

    # Environment
    ENVIRONMENT: str = "development"  # Default to development

    # LLM Settings
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: Optional[str] = "us-east-1"

    # Monitoring Configuration
    ENABLE_MONITORING: bool = False
    MONITORING_INTERVAL: int = 60

    class Config:
        case_sensitive = True
        env_file = os.getenv("ENV_FILE", ".env")
        extra = "ignore"  # Ignore extra fields

settings = Settings() 