from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, Field
import os
import json

class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./test.db"

    # AWS Configuration
    AWS_ACCESS_KEY_ID: str = "your_aws_access_key"
    AWS_SECRET_ACCESS_KEY: str = "your_aws_secret_key"
    AWS_REGION: str = "us-east-1"
    AWS_BUCKET_NAME: str = "openmcp-dev-bucket"
    S3_BUCKET: str = "openmcp-test-bucket"  # Default value for testing

    # JWT Configuration
    JWT_SECRET_KEY: str = "your_jwt_secret_key_here"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "OpenMCP Backend"
    VERSION: str = "0.1.0"

    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://127.0.0.1:3000"
        ]
    )

    # LLM Configuration
    LLM_PROVIDER: str = "openai"
    LLM_MODEL: str = "gpt-4"
    LLM_MAX_TOKENS: int = 2000
    LLM_TEMPERATURE: float = 0.7

    # Monitoring Configuration
    ENABLE_MONITORING: bool = True
    MONITORING_INTERVAL: int = 60
    PROMETHEUS_MULTIPROC_DIR: str = "./prometheus_data"
    SENTRY_DSN: str | None = None

    # Environment
    ENVIRONMENT: str = "development"  # Default to development

    class Config:
        case_sensitive = True
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), ".env")

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> any:
            if field_name == "BACKEND_CORS_ORIGINS":
                try:
                    return json.loads(raw_val)
                except:
                    return raw_val.split(",")
            return raw_val

settings = Settings() 