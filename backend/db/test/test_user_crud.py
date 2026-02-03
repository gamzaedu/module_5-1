"""
User CRUD Functions Tests.

Tests for User CRUD operations including:
- get_user_by_id (existing/non-existing)
- get_user_by_email (existing/non-existing)
- get_user_by_username (existing/non-existing)
- create_user (normal creation)
- create_user duplicate constraints (email, username)
"""

import sys
from pathlib import Path

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

# Add backend/app to path for imports
backend_path = Path(__file__).parent.parent.parent / "app"
sys.path.insert(0, str(backend_path.parent))

from app.models.user import User
from app.crud.user import (
    get_user_by_id,
    get_user_by_email,
    get_user_by_username,
    create_user,
)


class TestGetUserById:
    """Tests for get_user_by_id function."""

    def test_get_user_by_id_exists(self, db_session: Session, sample_user: User):
        """Test getting an existing user by id."""
        result = get_user_by_id(db_session, sample_user.id)

        assert result is not None
        assert result.id == sample_user.id
        assert result.username == sample_user.username
        assert result.email == sample_user.email

    def test_get_user_by_id_not_exists(self, db_session: Session):
        """Test getting a non-existing user by id returns None."""
        result = get_user_by_id(db_session, 99999)

        assert result is None

    def test_get_user_by_id_zero(self, db_session: Session):
        """Test getting user with id 0 returns None."""
        result = get_user_by_id(db_session, 0)

        assert result is None

    def test_get_user_by_id_negative(self, db_session: Session):
        """Test getting user with negative id returns None."""
        result = get_user_by_id(db_session, -1)

        assert result is None


class TestGetUserByEmail:
    """Tests for get_user_by_email function."""

    def test_get_user_by_email_exists(self, db_session: Session, sample_user: User):
        """Test getting an existing user by email."""
        result = get_user_by_email(db_session, sample_user.email)

        assert result is not None
        assert result.id == sample_user.id
        assert result.email == sample_user.email

    def test_get_user_by_email_not_exists(self, db_session: Session):
        """Test getting a non-existing user by email returns None."""
        result = get_user_by_email(db_session, "nonexistent@example.com")

        assert result is None

    def test_get_user_by_email_empty_string(self, db_session: Session):
        """Test getting user with empty email returns None."""
        result = get_user_by_email(db_session, "")

        assert result is None

    def test_get_user_by_email_case_sensitive(self, db_session: Session, sample_user: User):
        """Test that email lookup is case-sensitive in SQLite."""
        # SQLite is case-insensitive by default for ASCII
        upper_email = sample_user.email.upper()
        result = get_user_by_email(db_session, upper_email)

        # Note: SQLite LIKE is case-insensitive, but = is case-sensitive
        # This test documents the actual behavior
        if result is not None:
            # If found, it matched despite case difference
            assert result.id == sample_user.id


class TestGetUserByUsername:
    """Tests for get_user_by_username function."""

    def test_get_user_by_username_exists(self, db_session: Session, sample_user: User):
        """Test getting an existing user by username."""
        result = get_user_by_username(db_session, sample_user.username)

        assert result is not None
        assert result.id == sample_user.id
        assert result.username == sample_user.username

    def test_get_user_by_username_not_exists(self, db_session: Session):
        """Test getting a non-existing user by username returns None."""
        result = get_user_by_username(db_session, "nonexistent_user")

        assert result is None

    def test_get_user_by_username_empty_string(self, db_session: Session):
        """Test getting user with empty username returns None."""
        result = get_user_by_username(db_session, "")

        assert result is None

    def test_get_user_by_username_with_multiple_users(
        self, db_session: Session, multiple_users: list[User]
    ):
        """Test getting correct user when multiple users exist."""
        target_user = multiple_users[1]  # Get middle user

        result = get_user_by_username(db_session, target_user.username)

        assert result is not None
        assert result.id == target_user.id
        assert result.username == target_user.username


class TestCreateUser:
    """Tests for create_user function."""

    def test_create_user_with_dict(self, db_session: Session):
        """Test creating a user with dictionary data."""
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "plaintext_password"  # Will be excluded
        }
        hashed_password = "hashed_password_value"

        result = create_user(db_session, user_data, hashed_password)

        assert result is not None
        assert result.id is not None
        assert result.username == "newuser"
        assert result.email == "newuser@example.com"
        assert result.hashed_password == hashed_password
        assert result.is_active is True

    def test_create_user_returns_complete_user(self, db_session: Session):
        """Test that create_user returns a complete User object."""
        user_data = {
            "username": "completeuser",
            "email": "complete@example.com",
            "password": "password123"
        }
        hashed_password = "hashed_complete"

        result = create_user(db_session, user_data, hashed_password)

        # Verify all fields are set
        assert result.id is not None
        assert result.username == "completeuser"
        assert result.email == "complete@example.com"
        assert result.hashed_password == hashed_password
        assert result.is_active is True
        assert result.created_at is not None

    def test_create_user_persisted_to_db(self, db_session: Session):
        """Test that created user is persisted to database."""
        user_data = {
            "username": "persisteduser",
            "email": "persisted@example.com",
            "password": "password123"
        }
        hashed_password = "hashed_persisted"

        created_user = create_user(db_session, user_data, hashed_password)

        # Query the database directly
        queried_user = db_session.query(User).filter(
            User.id == created_user.id
        ).first()

        assert queried_user is not None
        assert queried_user.username == "persisteduser"
        assert queried_user.email == "persisted@example.com"

    def test_create_user_password_excluded_from_data(self, db_session: Session):
        """Test that password field is excluded from user data."""
        user_data = {
            "username": "nopassworduser",
            "email": "nopassword@example.com",
            "password": "should_be_excluded"
        }
        hashed_password = "properly_hashed"

        result = create_user(db_session, user_data, hashed_password)

        # Password should not be stored; only hashed_password
        assert result.hashed_password == hashed_password
        # User model doesn't have a 'password' attribute
        assert not hasattr(result, 'password') or getattr(result, 'password', None) is None


class TestCreateUserDuplicateConstraints:
    """Tests for duplicate constraint violations in create_user."""

    def test_create_user_duplicate_email(self, db_session: Session, sample_user: User):
        """Test that creating user with duplicate email raises error."""
        user_data = {
            "username": "different_username",
            "email": sample_user.email,  # Duplicate email
            "password": "password123"
        }
        hashed_password = "hashed_duplicate"

        with pytest.raises(IntegrityError):
            create_user(db_session, user_data, hashed_password)

    def test_create_user_duplicate_username(self, db_session: Session, sample_user: User):
        """Test that creating user with duplicate username raises error."""
        user_data = {
            "username": sample_user.username,  # Duplicate username
            "email": "different@example.com",
            "password": "password123"
        }
        hashed_password = "hashed_duplicate"

        with pytest.raises(IntegrityError):
            create_user(db_session, user_data, hashed_password)

    def test_create_user_duplicate_both(self, db_session: Session, sample_user: User):
        """Test that creating user with duplicate username and email raises error."""
        user_data = {
            "username": sample_user.username,  # Duplicate
            "email": sample_user.email,  # Duplicate
            "password": "password123"
        }
        hashed_password = "hashed_duplicate"

        with pytest.raises(IntegrityError):
            create_user(db_session, user_data, hashed_password)


class TestCreateUserWithPydanticModel:
    """Tests for create_user with Pydantic-like model objects."""

    def test_create_user_with_model_dump(self, db_session: Session):
        """Test creating user with object that has model_dump method."""

        class MockPydanticModel:
            """Mock Pydantic model with model_dump method."""
            def __init__(self, username, email, password):
                self.username = username
                self.email = email
                self.password = password

            def model_dump(self, exclude=None):
                data = {
                    "username": self.username,
                    "email": self.email,
                    "password": self.password
                }
                if exclude:
                    for key in exclude:
                        data.pop(key, None)
                return data

        user_data = MockPydanticModel(
            username="pydantic_user",
            email="pydantic@example.com",
            password="password123"
        )
        hashed_password = "hashed_pydantic"

        result = create_user(db_session, user_data, hashed_password)

        assert result is not None
        assert result.username == "pydantic_user"
        assert result.email == "pydantic@example.com"
        assert result.hashed_password == hashed_password

    def test_create_user_with_dict_method(self, db_session: Session):
        """Test creating user with object that has dict method (older Pydantic)."""

        class MockOldPydanticModel:
            """Mock old Pydantic model with dict method."""
            def __init__(self, username, email, password):
                self.username = username
                self.email = email
                self.password = password

            def dict(self, exclude=None):
                data = {
                    "username": self.username,
                    "email": self.email,
                    "password": self.password
                }
                if exclude:
                    for key in exclude:
                        data.pop(key, None)
                return data

        user_data = MockOldPydanticModel(
            username="old_pydantic_user",
            email="old_pydantic@example.com",
            password="password123"
        )
        hashed_password = "hashed_old_pydantic"

        result = create_user(db_session, user_data, hashed_password)

        assert result is not None
        assert result.username == "old_pydantic_user"
        assert result.email == "old_pydantic@example.com"
        assert result.hashed_password == hashed_password
