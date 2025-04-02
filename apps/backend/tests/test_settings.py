import os
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings

# Set test environment file path before any other imports
test_env_path = Path(__file__).parent / ".env.test"
os.environ["ENV_FILE"] = str(test_env_path)

class TestSettings(BaseSettings):
    # Database
    DATABASE_URL: str

    # AWS
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str
    AWS_BUCKET_NAME: str

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # API
    API_V1_STR: str
    PROJECT_NAME: str
    VERSION: str

    # CORS
    BACKEND_CORS_ORIGINS: List[str]

    # Monitoring
    ENABLE_MONITORING: bool
    MONITORING_INTERVAL: int

    class Config:
        env_file = os.getenv("ENV_FILE", ".env.test")
        case_sensitive = True

# Create a global settings instance
settings = TestSettings() 