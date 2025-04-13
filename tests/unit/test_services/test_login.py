from unittest.mock import patch

import pytest

from app.common.result import Failure, Success
from app.errors.authentication_errors import InvalidCredentialsError
from app.schemas.auth_request import AuthRequest
from app.services.login_with_email import verify_email_and_password


class TestLoginService:
    @pytest.fixture
    def auth_request(self):
        return AuthRequest(email="test@example.com", password="password123")

    @patch("app.services.login_with_email.requests.post")
    def test_login_success(self, mock_post, auth_request):
        # Setup mock response
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"idToken": "test-token"}

        # Call the function
        result = verify_email_and_password(auth_request)
        # Verify results
        assert isinstance(result, Success)
        assert result.value == "test-token"

        # Verify the mock was called with correct URL from env var
        mock_post.assert_called_once()
        url, kwargs = mock_post.call_args
        assert "mock-firebase-auth-url" in url[0]
        assert "email" in kwargs["json"]
        assert "password" in kwargs["json"]

    @patch("app.services.login_with_email.requests.post")
    def test_login_failure(self, mock_post, auth_request):
        # Setup mock response
        mock_response = mock_post.return_value
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "error": {"message": "Invalid email or password"}
        }

        # Call the function
        result = verify_email_and_password(auth_request)
        # Verify results
        assert isinstance(result, Failure)
        assert isinstance(result.error, InvalidCredentialsError)
        assert (
            result.error.message == "Authentication failed: Invalid email or password"
        )
