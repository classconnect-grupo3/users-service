import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from firebase_admin import auth as firebase_auth

from app.common.result import Success, Failure
from app.common.constants import NEW_USER, OLD_USER
from app.errors.firebase_errors import (
    InvalidIdTokenError,
    ExpiredIdTokenError,
    RevokedIdTokenError,
    CertificateFetchError,
    UserDisabledError,
    ArgumentsMissingError,
)
from app.services.login_with_google import authenticate_with_google

# Mock data
MOCK_ID_TOKEN = "mock_id_token"
MOCK_UID = "mock_uid"
MOCK_EMAIL = "test@example.com"
MOCK_NAME = "John Doe"


@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)


class TestAuthenticateWithGoogle:

    @patch("app.services.login_with_google.firebase_auth")
    @patch("app.services.login_with_google.get_user_by_email_db")
    def test_authenticate_with_google_success_new_user(
        self, mock_get_user, mock_firebase_auth, mock_db
    ):
        # Arrange
        mock_firebase_auth.verify_id_token.return_value = {
            "uid": MOCK_UID,
            "email": MOCK_EMAIL,
            "name": MOCK_NAME,
        }
        mock_get_user.return_value = None  # User doesn't exist

        # Act
        result = authenticate_with_google(MOCK_ID_TOKEN, mock_db)

        # Assert
        assert isinstance(result, Success)
        assert result.value == NEW_USER
        mock_firebase_auth.verify_id_token.assert_called_once_with(MOCK_ID_TOKEN)
        mock_get_user.assert_called_once_with(mock_db, MOCK_EMAIL)

    @patch("app.services.login_with_google.firebase_auth")
    @patch("app.services.login_with_google.get_user_by_email_db")
    def test_authenticate_with_google_success_existing_user(
        self, mock_get_user, mock_firebase_auth, mock_db
    ):
        # Arrange
        mock_firebase_auth.verify_id_token.return_value = {
            "uid": MOCK_UID,
            "email": MOCK_EMAIL,
            "name": MOCK_NAME,
        }
        mock_get_user.return_value = MagicMock()  # User exists

        # Act
        result = authenticate_with_google(MOCK_ID_TOKEN, mock_db)

        # Assert
        assert isinstance(result, Success)
        assert result.value == OLD_USER
        mock_firebase_auth.verify_id_token.assert_called_once_with(MOCK_ID_TOKEN)
        mock_get_user.assert_called_once_with(mock_db, MOCK_EMAIL)

    @patch("app.services.login_with_google.firebase_auth")
    def test_authenticate_with_google_invalid_token(self, mock_firebase_auth, mock_db):
        # Arrange
        mock_firebase_auth.verify_id_token.side_effect = Exception("Invalid ID token")

        # Act
        result = authenticate_with_google(MOCK_ID_TOKEN, mock_db)

        # Assert
        assert isinstance(result, Failure)
        assert isinstance(result.error, InvalidIdTokenError)
        assert result.error.http_status_code == 401
        mock_firebase_auth.verify_id_token.assert_called_once_with(MOCK_ID_TOKEN)

    @patch("app.services.login_with_google.firebase_auth")
    def test_authenticate_with_google_expired_token(self, mock_firebase_auth, mock_db):
        # Arrange
        mock_firebase_auth.verify_id_token.side_effect = Exception("Token expired")

        # Act
        result = authenticate_with_google(MOCK_ID_TOKEN, mock_db)

        # Assert
        assert isinstance(result, Failure)
        assert isinstance(result.error, ExpiredIdTokenError)
        assert result.error.http_status_code == 401
        mock_firebase_auth.verify_id_token.assert_called_once_with(MOCK_ID_TOKEN)

    @patch("app.services.login_with_google.firebase_auth")
    def test_authenticate_with_google_revoked_token(self, mock_firebase_auth, mock_db):
        # Arrange
        mock_firebase_auth.verify_id_token.side_effect = Exception(
            "Token has been revoked"
        )

        # Act
        result = authenticate_with_google(MOCK_ID_TOKEN, mock_db)

        # Assert
        assert isinstance(result, Failure)
        assert isinstance(result.error, RevokedIdTokenError)
        assert result.error.http_status_code == 401
        mock_firebase_auth.verify_id_token.assert_called_once_with(MOCK_ID_TOKEN)

    @patch("app.services.login_with_google.firebase_auth")
    def test_authenticate_with_google_certificate_error(
        self, mock_firebase_auth, mock_db
    ):
        # Arrange
        mock_firebase_auth.verify_id_token.side_effect = Exception(
            "Failed to fetch certificate"
        )

        # Act
        result = authenticate_with_google(MOCK_ID_TOKEN, mock_db)

        # Assert
        assert isinstance(result, Failure)
        assert isinstance(result.error, CertificateFetchError)
        assert result.error.http_status_code == 500
        mock_firebase_auth.verify_id_token.assert_called_once_with(MOCK_ID_TOKEN)

    @patch("app.services.login_with_google.firebase_auth")
    def test_authenticate_with_google_user_disabled(self, mock_firebase_auth, mock_db):
        # Arrange
        mock_firebase_auth.verify_id_token.side_effect = Exception("User is disabled")

        # Act
        result = authenticate_with_google(MOCK_ID_TOKEN, mock_db)

        # Assert
        assert isinstance(result, Failure)
        assert isinstance(result.error, UserDisabledError)
        assert result.error.http_status_code == 403
        mock_firebase_auth.verify_id_token.assert_called_once_with(MOCK_ID_TOKEN)

    @patch("app.services.login_with_google.firebase_auth")
    def test_authenticate_with_google_missing_uid(self, mock_firebase_auth, mock_db):
        # Arrange
        mock_firebase_auth.verify_id_token.return_value = {
            "email": MOCK_EMAIL,
            "name": MOCK_NAME,
        }

        # Act
        result = authenticate_with_google(MOCK_ID_TOKEN, mock_db)

        # Assert
        assert isinstance(result, Failure)
        assert isinstance(result.error, ArgumentsMissingError)
        assert result.error.http_status_code == 401
        assert "UID or email not found in token" in str(result.error)
        mock_firebase_auth.verify_id_token.assert_called_once_with(MOCK_ID_TOKEN)

    @patch("app.services.login_with_google.firebase_auth")
    def test_authenticate_with_google_missing_email(self, mock_firebase_auth, mock_db):
        # Arrange
        mock_firebase_auth.verify_id_token.return_value = {
            "uid": MOCK_UID,
            "name": MOCK_NAME,
        }

        # Act
        result = authenticate_with_google(MOCK_ID_TOKEN, mock_db)

        # Assert
        assert isinstance(result, Failure)
        assert isinstance(result.error, ArgumentsMissingError)
        assert result.error.http_status_code == 401
        assert "UID or email not found in token" in str(result.error)
        mock_firebase_auth.verify_id_token.assert_called_once_with(MOCK_ID_TOKEN)
