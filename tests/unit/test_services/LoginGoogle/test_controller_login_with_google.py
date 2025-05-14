from app.common.constants import NEW_USER, OLD_USER
import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.controllers.login_with_google import login_with_google
from app.schemas.token import Token
from app.schemas.google_auth_result import GoogleAuthResult
from app.common.result import Success, Failure
from app.errors.firebase_errors import InvalidIdTokenError

# Mock data
MOCK_ID_TOKEN = "mock_id_token"


@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)


@pytest.fixture
def mock_token():
    return Token(id_token=MOCK_ID_TOKEN)


class TestLoginWithGoogle:

    @patch("app.controllers.login_with_google.authenticate_with_google")
    def test_login_with_google_success_new_user(
        self, mock_authenticate, mock_db, mock_token
    ):
        # Arrange
        mock_authenticate.return_value = Success(NEW_USER)

        # Act
        result = login_with_google(mock_token, mock_db)

        # Assert
        assert isinstance(result, GoogleAuthResult)
        assert result.id_token == MOCK_ID_TOKEN
        assert result.was_already_registered == False # False indicates new user
        mock_authenticate.assert_called_once_with(MOCK_ID_TOKEN, mock_db)

    @patch("app.controllers.login_with_google.authenticate_with_google")
    def test_login_with_google_success_existing_user(
        self, mock_authenticate, mock_db, mock_token
    ):
        # Arrange
        mock_authenticate.return_value = Success(OLD_USER)

        # Act
        result = login_with_google(mock_token, mock_db)

        # Assert
        assert isinstance(result, GoogleAuthResult)
        assert result.id_token == MOCK_ID_TOKEN
        assert result.was_already_registered == True # True indicates existing user
        mock_authenticate.assert_called_once_with(MOCK_ID_TOKEN, mock_db)

    @patch("app.controllers.login_with_google.authenticate_with_google")
    def test_login_with_google_invalid_token(
        self, mock_authenticate, mock_db, mock_token
    ):
        # Arrange
        mock_authenticate.return_value = Failure(InvalidIdTokenError())

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            login_with_google(mock_token, mock_db)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "The id_token is not a valid Firebase ID token."
        mock_authenticate.assert_called_once_with(MOCK_ID_TOKEN, mock_db)

    @patch("app.controllers.login_with_google.authenticate_with_google")
    def test_login_with_google_expired_token(
        self, mock_authenticate, mock_db, mock_token
    ):
        # Arrange
        from app.errors.firebase_errors import ExpiredIdTokenError

        mock_authenticate.return_value = Failure(ExpiredIdTokenError())

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            login_with_google(mock_token, mock_db)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "The ID token has expired."
        mock_authenticate.assert_called_once_with(MOCK_ID_TOKEN, mock_db)

    @patch("app.controllers.login_with_google.authenticate_with_google")
    def test_login_with_google_revoked_token(
        self, mock_authenticate, mock_db, mock_token
    ):
        # Arrange
        from app.errors.firebase_errors import RevokedIdTokenError

        mock_authenticate.return_value = Failure(RevokedIdTokenError())

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            login_with_google(mock_token, mock_db)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "The ID token has been revoked."
        mock_authenticate.assert_called_once_with(MOCK_ID_TOKEN, mock_db)
