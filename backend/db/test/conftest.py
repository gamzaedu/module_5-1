"""
pytest fixtures for database tests.

Provides test database session, engine, and test data fixtures.
Uses SQLite in-memory database for isolation and speed.
"""

import sys
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

# Add backend/app to path for imports
backend_path = Path(__file__).parent.parent.parent / "app"
sys.path.insert(0, str(backend_path.parent))

from app.database import Base
from app.models.user import User


# Test database URL - SQLite in-memory
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def test_engine():
    """Create a test database engine with in-memory SQLite.

    Uses StaticPool to ensure the same connection is reused,
    which is necessary for in-memory SQLite databases.
    """
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create all tables
    Base.metadata.create_all(bind=engine)

    yield engine

    # Drop all tables after test
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(test_engine) -> Session:
    """Create a test database session.

    Each test gets a fresh session with transaction rollback
    to ensure test isolation.
    """
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def sample_user_data() -> dict:
    """Sample user data for testing."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "hashed_password": "hashed_password_123"
    }


@pytest.fixture
def sample_user(db_session: Session, sample_user_data: dict) -> User:
    """Create a sample user in the test database."""
    user = User(**sample_user_data)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def multiple_users(db_session: Session) -> list[User]:
    """Create multiple users for testing list operations."""
    users_data = [
        {"username": "user1", "email": "user1@example.com", "hashed_password": "hash1"},
        {"username": "user2", "email": "user2@example.com", "hashed_password": "hash2"},
        {"username": "user3", "email": "user3@example.com", "hashed_password": "hash3"},
    ]

    users = []
    for data in users_data:
        user = User(**data)
        db_session.add(user)
        users.append(user)

    db_session.commit()

    for user in users:
        db_session.refresh(user)

    return users
