from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "MCP Server"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # LLM Configuration
    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: str
    DEFAULT_LLM_PROVIDER: str = "openai"
    MAX_TOKENS: int = 2000

    # Environment Configuration
    ENVIRONMENT: str = "development"  # development, integration, production
    
    # Database Configuration
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "openmcp"
    
    @property
    def DATABASE_URL(self) -> str:
        if self.ENVIRONMENT == "development":
            return "sqlite:///./test.db"
        elif self.ENVIRONMENT == "integration":
            return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        else:  # production
            return os.getenv("DATABASE_URL", "")  # Use external database URL for production

    # Storage Configuration
    @property
    def STORAGE_CONFIG(self) -> dict:
        if self.ENVIRONMENT in ["development", "integration"]:
            return {
                "type": "local",
                "base_path": "./data"  # Local storage path for development and integration
            }
        else:  # production
            return {
                "type": "s3",
                "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID", ""),
                "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY", ""),
                "aws_region": os.getenv("AWS_REGION", "us-east-1"),
                "bucket_name": os.getenv("S3_BUCKET_NAME", "")
            }
    
    # Monitoring Configuration
    ENABLE_MONITORING: bool = False
    MONITORING_INTERVAL: int = 60

    class Config:
        case_sensitive = True
        env_file = os.getenv("ENV_FILE", ".env")
        extra = "ignore"  # This will ignore any extra fields in the environment

settings = Settings() 