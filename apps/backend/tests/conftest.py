import os
from pathlib import Path
import sys

# Add src directory to Python path before any other imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Set test environment file path
test_env_path = Path(__file__).parent / ".env.test"
os.environ["ENV_FILE"] = str(test_env_path)

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from fastapi import FastAPI, Depends
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.services.context import ContextService
from app.services.test_storage import TestStorageService
from app.services.storage import StorageService
from app.api.v1.endpoints.context import get_context_service
from tests.test_settings import settings

# Test database URLs
SQLITE_DB_URL = "sqlite:///./test.db"
POSTGRES_DB_URL = "postgresql://test_user:test_password@localhost:5432/test_db"

@pytest.fixture(scope="session")
def db_type(request):
    """Fixture to select database type for tests."""
    return request.config.getoption("--db-type", default="sqlite")

@pytest.fixture(scope="session")
def db_url(db_type):
    """Fixture to get database URL based on type."""
    return SQLITE_DB_URL if db_type == "sqlite" else POSTGRES_DB_URL

@pytest.fixture(scope="session")
def engine(db_url):
    """Create test database engine."""
    engine = create_engine(db_url)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db(engine):
    """Create a fresh database session for each test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db, storage_service):
    """Create a test client with a fresh database session."""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    def override_get_context_service(db: Session = Depends(get_db)) -> ContextService:
        return ContextService(db, storage_service)
    
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_context_service] = override_get_context_service
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def context_service(db, storage_service):
    """Create a context service instance."""
    return ContextService(db, storage_service)

@pytest.fixture(scope="function")
def storage_service(request):
    """Create a storage service instance based on test mode."""
    if request.config.getoption("--cloud", default=False):
        service = StorageService()
    else:
        service = TestStorageService()
    yield service
    if isinstance(service, TestStorageService):
        service.cleanup()

def pytest_addoption(parser):
    """Add command line options for pytest."""
    parser.addoption(
        "--db-type",
        action="store",
        default="sqlite",
        help="Database type for tests (sqlite or postgres)",
    )
    parser.addoption(
        "--cloud",
        action="store_true",
        default=False,
        help="Use cloud storage instead of local test storage",
    ) 