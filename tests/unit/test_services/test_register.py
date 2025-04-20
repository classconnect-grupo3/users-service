from unittest.mock import patch, MagicMock

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.db import Base
from app.models.user_model import User

from app.common.result import Success
from app.schemas.user import UserBase
from app.services.register import create_new_user


@pytest.fixture(scope="function")
def db_engine():
    """Create a SQLAlchemy engine with SQLite in memory."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Create a new database session for each test."""
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.close()


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

    @pytest.fixture
    def mock_db(self):
        # Create a mock database session
        mock_session = MagicMock()

        # Configure the mock to return None for any query.filter operations
        # This simulates an empty result when searching for a user
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = None
        mock_session.query.return_value = mock_query

        return mock_session

    @pytest.mark.asyncio
    @patch("app.services.register.create_firebase_user")
    async def test_create_user_success(
        self, mock_create_firebase_user, user,  db_session
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
