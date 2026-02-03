"""
User Model Tests.

Tests for User SQLAlchemy model including:
- Table creation
- Primary key constraints
- Unique constraints (username, email)
- Index creation
- Field constraints (nullable, max_length)
- Default values (is_active=True)
- Timestamp auto-setting (created_at, updated_at)
"""

import sys
from pathlib import Path
from datetime import datetime

import pytest
from sqlalchemy import inspect, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

# Add backend/app to path for imports
backend_path = Path(__file__).parent.parent.parent / "app"
sys.path.insert(0, str(backend_path.parent))

from app.models.user import User
from app.database import Base


class TestUserTableCreation:
    """Tests for User table creation and structure."""

    def test_table_exists(self, test_engine):
        """Test that users table is created."""
        inspector = inspect(test_engine)
        tables = inspector.get_table_names()
        assert "users" in tables

    def test_table_has_correct_columns(self, test_engine):
        """Test that users table has all expected columns."""
        inspector = inspect(test_engine)
        columns = {col["name"] for col in inspector.get_columns("users")}

        expected_columns = {
            "id", "username", "email", "hashed_password",
            "is_active", "created_at", "updated_at"
        }
        assert expected_columns == columns


class TestUserPrimaryKey:
    """Tests for User primary key."""

    def test_primary_key_exists(self, test_engine):
        """Test that id column is primary key."""
        inspector = inspect(test_engine)
        pk_constraint = inspector.get_pk_constraint("users")
        assert "id" in pk_constraint["constrained_columns"]

    def test_primary_key_auto_increment(self, db_session: Session):
        """Test that id auto-increments."""
        user1 = User(
            username="user1",
            email="user1@test.com",
            hashed_password="hash1"
        )
        user2 = User(
            username="user2",
            email="user2@test.com",
            hashed_password="hash2"
        )

        db_session.add(user1)
        db_session.commit()
        db_session.refresh(user1)

        db_session.add(user2)
        db_session.commit()
        db_session.refresh(user2)

        assert user1.id is not None
        assert user2.id is not None
        assert user2.id > user1.id


class TestUserUniqueConstraints:
    """Tests for unique constraints on username and email."""

    def test_username_unique_constraint(self, db_session: Session, sample_user: User):
        """Test that duplicate username raises IntegrityError."""
        duplicate_user = User(
            username=sample_user.username,  # Same username
            email="different@test.com",
            hashed_password="hash"
        )

        db_session.add(duplicate_user)

        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_email_unique_constraint(self, db_session: Session, sample_user: User):
        """Test that duplicate email raises IntegrityError."""
        duplicate_user = User(
            username="different_user",
            email=sample_user.email,  # Same email
            hashed_password="hash"
        )

        db_session.add(duplicate_user)

        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_different_username_and_email_allowed(self, db_session: Session, sample_user: User):
        """Test that different username and email are allowed."""
        new_user = User(
            username="newuser",
            email="new@test.com",
            hashed_password="hash"
        )

        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)

        assert new_user.id is not None


class TestUserIndexes:
    """Tests for index creation on User table."""

    def test_id_index_exists(self, test_engine):
        """Test that id column has index."""
        inspector = inspect(test_engine)
        indexes = inspector.get_indexes("users")

        # id is primary key, which creates implicit index
        pk_constraint = inspector.get_pk_constraint("users")
        assert "id" in pk_constraint["constrained_columns"]

    def test_username_index_exists(self, test_engine):
        """Test that username column has index."""
        inspector = inspect(test_engine)
        indexes = inspector.get_indexes("users")

        username_indexed = any(
            "username" in idx.get("column_names", [])
            for idx in indexes
        )
        assert username_indexed, "username should have an index"

    def test_email_index_exists(self, test_engine):
        """Test that email column has index."""
        inspector = inspect(test_engine)
        indexes = inspector.get_indexes("users")

        email_indexed = any(
            "email" in idx.get("column_names", [])
            for idx in indexes
        )
        assert email_indexed, "email should have an index"


class TestUserFieldConstraints:
    """Tests for field constraints (nullable, max_length)."""

    def test_username_not_nullable(self, db_session: Session):
        """Test that username cannot be null."""
        user = User(
            username=None,
            email="test@test.com",
            hashed_password="hash"
        )

        db_session.add(user)

        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_email_not_nullable(self, db_session: Session):
        """Test that email cannot be null."""
        user = User(
            username="testuser",
            email=None,
            hashed_password="hash"
        )

        db_session.add(user)

        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_hashed_password_not_nullable(self, db_session: Session):
        """Test that hashed_password cannot be null."""
        user = User(
            username="testuser",
            email="test@test.com",
            hashed_password=None
        )

        db_session.add(user)

        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_username_max_length(self, test_engine):
        """Test that username has max length constraint."""
        inspector = inspect(test_engine)
        columns = {col["name"]: col for col in inspector.get_columns("users")}

        # String(50) in model
        username_col = columns["username"]
        assert username_col["type"].length == 50

    def test_email_max_length(self, test_engine):
        """Test that email has max length constraint."""
        inspector = inspect(test_engine)
        columns = {col["name"]: col for col in inspector.get_columns("users")}

        # String(100) in model
        email_col = columns["email"]
        assert email_col["type"].length == 100

    def test_hashed_password_max_length(self, test_engine):
        """Test that hashed_password has max length constraint."""
        inspector = inspect(test_engine)
        columns = {col["name"]: col for col in inspector.get_columns("users")}

        # String(255) in model
        hashed_password_col = columns["hashed_password"]
        assert hashed_password_col["type"].length == 255


class TestUserDefaultValues:
    """Tests for default values."""

    def test_is_active_default_true(self, db_session: Session):
        """Test that is_active defaults to True."""
        user = User(
            username="testuser",
            email="test@test.com",
            hashed_password="hash"
        )

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        assert user.is_active is True

    def test_is_active_can_be_set_false(self, db_session: Session):
        """Test that is_active can be explicitly set to False."""
        user = User(
            username="testuser",
            email="test@test.com",
            hashed_password="hash",
            is_active=False
        )

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        assert user.is_active is False


class TestUserTimestamps:
    """Tests for timestamp auto-setting (created_at, updated_at)."""

    def test_created_at_auto_set(self, db_session: Session):
        """Test that created_at is automatically set on creation."""
        before_create = datetime.utcnow()

        user = User(
            username="testuser",
            email="test@test.com",
            hashed_password="hash"
        )

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        after_create = datetime.utcnow()

        assert user.created_at is not None
        # Allow some tolerance for timing
        assert before_create <= user.created_at.replace(tzinfo=None) <= after_create or \
               abs((user.created_at.replace(tzinfo=None) - before_create).total_seconds()) < 5

    def test_updated_at_initially_none(self, db_session: Session):
        """Test that updated_at is None initially (only set on update)."""
        user = User(
            username="testuser",
            email="test@test.com",
            hashed_password="hash"
        )

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # updated_at uses onupdate, so it's None initially
        assert user.updated_at is None

    def test_updated_at_set_on_update(self, db_session: Session):
        """Test that updated_at is set when record is updated."""
        user = User(
            username="testuser",
            email="test@test.com",
            hashed_password="hash"
        )

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # Initial updated_at should be None
        assert user.updated_at is None

        # Update the user
        user.username = "updated_username"
        db_session.commit()
        db_session.refresh(user)

        # updated_at should now be set
        assert user.updated_at is not None

    def test_created_at_not_changed_on_update(self, db_session: Session):
        """Test that created_at is not changed when record is updated."""
        user = User(
            username="testuser",
            email="test@test.com",
            hashed_password="hash"
        )

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        original_created_at = user.created_at

        # Update the user
        user.username = "updated_username"
        db_session.commit()
        db_session.refresh(user)

        # created_at should remain unchanged
        assert user.created_at == original_created_at
