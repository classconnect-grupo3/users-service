from unittest.mock import patch, MagicMock

import pytest

from app.errors.register_errors import UserAlreadyExists
from app.models.user_model import User

from app.common.result import Failure, Success
from app.schemas.user import UserBase
from app.services.register import create_new_user
from app.repositories.users import get_user_by_email_db


class TestRegisterService:

    @pytest.fixture
    def user(self):
        return UserBase(
            name="John",
            surname="Doe",
            email="john.doe@example.com",
            password="password123",
        )

    @pytest.fixture
    def null_user(self):
        return UserBase(
            name=None,
            surname=None,
            email=None,
            password=None,
        )

    @pytest.mark.asyncio
    @patch("app.services.register.create_firebase_user")
    async def test_create_user_success(
        self, mock_create_firebase_user, user, db_session
    ):
        # Setup mock Firebase user
        mock_user = MagicMock()
        mock_user.uid = "test-uid"

        # Mock the Firebase user creation
        mock_create_firebase_user.return_value = Success(mock_user)

        # Call the function with the real session
        result = await create_new_user(db_session, user)

        # Assert results
        assert isinstance(result, Success)

        # Verify database operations worked correctly
        created_user = db_session.query(User).filter_by(email=user.email).first()
        assert created_user is not None
        assert created_user.uid == "test-uid"

        # Verify the mock was called correctly
        mock_create_firebase_user.assert_called_once_with(user.email, user.password)

        # Delete the user from the database
        db_session.query(User).filter_by(email=user.email).delete()
        db_session.commit()

    @pytest.mark.asyncio
    @patch("app.services.register.create_firebase_user")
    async def test_create_user_failure(
        self, mock_create_firebase_user, user, db_session
    ):
        # Setup mock Firebase user creation to fail
        mock_create_firebase_user.return_value = Failure(
            "Failed to create Firebase user"
        )

        # Call the function with the real session
        result = await create_new_user(db_session, user)

        # Assert results
        assert isinstance(result, Failure)
        assert result.error == "Failed to create Firebase user"

        # Verify database operations were not performed
        assert db_session.query(User).filter_by(email=user.email).first() is None

        # Verify the mock was called correctly
        mock_create_firebase_user.assert_called_once_with(user.email, user.password)

        # Delete the user from the database
        db_session.query(User).filter_by(email=user.email).delete()
        db_session.commit()

    @pytest.mark.asyncio
    @patch("app.services.register.create_firebase_user")
    async def test_create_user_failure_with_existing_user(
        self, mock_create_firebase_user, user, db_session
    ):
        # Setup mock Firebase user
        mock_user = MagicMock()
        mock_user.uid = "test-uid"
        mock_create_firebase_user.return_value = Success(mock_user)

        # Create a user in the database
        result = await create_new_user(db_session, user)

        # Assert results
        assert isinstance(result, Success)

        # Verify database operations worked correctly
        userInstance = get_user_by_email_db(db_session, user.email)
        assert userInstance is not None
        assert userInstance.email == user.email

        # Try to create the same user again
        result = await create_new_user(db_session, user)
        assert isinstance(result, Failure)
        assert isinstance(result.error, UserAlreadyExists)

        # Delete the user from the database
        db_session.query(User).filter_by(email=user.email).delete()
        db_session.commit()
