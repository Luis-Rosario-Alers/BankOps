import time
from datetime import datetime, timezone
from unittest.mock import MagicMock, call, patch

import pytest
import requests

from src.services.session_manager import SessionManager

BASE_URL = " http://127.0.0.1:5000/api/v1/"
LOGIN_URL = f"{BASE_URL}auth/sessions/users"
REFRESH_URL = f"{BASE_URL}auth/sessions/renew"
LOGOUT_URL = f"{BASE_URL}auth/sessions/users"
DEFAULT_TIMEOUT = 5
KEYRING_SERVICE = "BankOpsBanking"


class TestSessionManager:
    @pytest.fixture
    def session_manager(self):
        session_manager = SessionManager()
        session_manager.base_url = BASE_URL
        session_manager.timeout = DEFAULT_TIMEOUT
        session_manager.access_token = None
        session_manager.refresh_token = None
        session_manager.base_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        yield session_manager

    # --- Mock Fixtures ---
    @pytest.fixture(autouse=True)
    def mock_keyring(self):
        """Auto-used fixture to mock keyring for all tests in this class."""
        with patch(
            "src.services.session_manager.keyring", autospec=True
        ) as mock_keyring:
            yield mock_keyring

    @pytest.fixture
    def mock_requests_post(self):
        with patch("src.services.session_manager.requests.post") as mock_post:
            yield mock_post

    @pytest.fixture
    def mock_requests_get(self):
        with patch("src.services.session_manager.requests.get") as mock_get:
            yield mock_get

    @pytest.fixture
    def mock_requests_delete(self):
        with patch("src.services.session_manager.requests.delete") as mock_delete:
            yield mock_delete

    # --- Helper ---
    def set_authenticated_state(
        self, session_manager, access_token="test_token", refresh_token="test_refresh"
    ):
        """Helper to set the access_token and header for tests requiring auth."""
        session_manager.access_token = access_token
        session_manager.refresh_token = refresh_token

    # --- Test _get_current_auth_header ---
    def test__get_current_auth_header_with_token(self, session_manager, mock_keyring):
        # Arrange
        mock_keyring.get_password.return_value = "valid_token"

        self.set_authenticated_state(session_manager, access_token="valid_token")

        # Act
        header = session_manager._get_current_auth_header()

        # Assert
        assert header == {"Authorization": "Bearer valid_token"}

    def test__get_current_auth_header_without_token(
        self, session_manager, mock_keyring
    ):
        # Arrange
        mock_keyring.get_password.return_value = None

        # Act
        header = session_manager._get_current_auth_header()

        # Assert
        assert header == {}

    # --- Test Keyring/Storage methods ---
    def test_store_token(self, session_manager, mock_keyring):
        # Arrange
        access_token = "new_access"
        refresh_token = "new_refresh"
        access_expire_ts = str(int(time.time() + 3600))
        refresh_expire_ts = str(int(time.time() + 86400))

        # Act
        session_manager.store_token(
            access_token, access_expire_ts, refresh_token, refresh_expire_ts
        )

        # Assert
        assert session_manager.access_token == access_token
        assert session_manager.refresh_token == refresh_token
        mock_keyring.set_password.assert_has_calls(
            [
                call(KEYRING_SERVICE, "access_token", access_token),
                call(KEYRING_SERVICE, "access_token_expire_time", access_expire_ts),
                call(KEYRING_SERVICE, "refresh_token", refresh_token),
                call(KEYRING_SERVICE, "refresh_token_expire_time", refresh_expire_ts),
            ],
            any_order=False,
        )  # Order matters here based on implementation
        assert mock_keyring.set_password.call_count == 4

    def test_get_access_token(self, session_manager, mock_keyring):
        # Arrange
        mock_keyring.get_password.return_value = "stored_access_token"

        # Act
        token = session_manager.get_access_token()

        # Assert
        mock_keyring.get_password.assert_called_with(KEYRING_SERVICE, "access_token")
        assert token == "stored_access_token"

    def test_get_refresh_token(self, session_manager, mock_keyring):
        # Arrange
        mock_keyring.get_password.return_value = "stored_refresh_token"

        # Act
        token = session_manager.get_refresh_token()

        # Assert
        mock_keyring.get_password.assert_called_with(KEYRING_SERVICE, "refresh_token")
        assert token == "stored_refresh_token"

    @patch("src.services.session_manager.logger", autospec=True)
    def test_clear_tokens(self, mock_logger, session_manager, mock_keyring):
        # Arrange
        self.set_authenticated_state(session_manager)  # Give it some tokens initially

        # Act
        session_manager.clear_tokens()

        # Assert
        mock_keyring.delete_password.assert_has_calls(
            [
                call(KEYRING_SERVICE, "access_token"),
                call(KEYRING_SERVICE, "refresh_token"),
                call(KEYRING_SERVICE, "access_token_expire_time"),
                call(KEYRING_SERVICE, "refresh_token_expire_time"),
            ],
            any_order=True,
        )  # Order might not strictly matter
        assert mock_keyring.delete_password.call_count == 4
        assert session_manager.access_token is None
        assert session_manager.refresh_token is None
        mock_logger.info.assert_called_with("JWT access_token cleared.")

    # --- Test check_expiration ---
    def test_check_expiration_no_token(self, session_manager, mock_keyring):
        # Arrange
        mock_keyring.get_password.return_value = None

        # Act
        is_expired = session_manager.check_expiration()

        # Assert
        mock_keyring.get_password.assert_called_with(
            KEYRING_SERVICE, "access_token_expire_time"
        )
        assert is_expired is True

    def test_check_expiration_expired(self, session_manager, mock_keyring):
        # Arrange
        past_timestamp = str(
            int(datetime.now(timezone.utc).timestamp() - 60)
        )  # 1 minute ago
        mock_keyring.get_password.return_value = past_timestamp

        # Act
        is_expired = session_manager.check_expiration()

        # Assert
        assert is_expired is True

    def test_check_expiration_not_expired(self, session_manager, mock_keyring):
        # Arrange
        future_timestamp = str(
            int(datetime.now(timezone.utc).timestamp() + 3600)
        )  # 1 hour from now
        mock_keyring.get_password.return_value = future_timestamp

        # Act
        is_expired = session_manager.check_expiration()

        # Assert
        assert is_expired is False

    @patch("src.services.session_manager.logger", autospec=True)
    def test_check_expiration_invalid_format(
        self, mock_logger, session_manager, mock_keyring
    ):
        # Arrange
        invalid_timestamp = "not-a-timestamp"
        mock_keyring.get_password.return_value = invalid_timestamp
        # Mock clear_tokens which gets called internally
        with patch.object(session_manager, "clear_tokens") as mock_clear:
            # Act
            is_expired = session_manager.check_expiration()

            # Assert
            assert is_expired is True
            mock_logger.error.assert_called_with(
                f"Invalid expiration format stored: {invalid_timestamp}"
            )
            mock_clear.assert_called_once()

    # --- Test attempt_session_refresh ---
    @patch("src.services.session_manager.datetime", wraps=datetime)
    def test_attempt_session_refresh_success(
        self, mock_datetime, session_manager, mock_requests_post, mock_keyring
    ):
        # Arrange
        mock_now = datetime.now(timezone.utc)
        mock_datetime.now.return_value = mock_now

        refresh_token = "valid_refresh_token"
        response = MagicMock()
        response.status_code = 200
        new_access = "new_access_token"
        new_refresh = "new_refresh_token"
        access_expires_ts = int(mock_now.timestamp()) + 3600
        refresh_expires_ts = int(mock_now.timestamp()) + 86400
        response.json.return_value = {
            "access_token": new_access,
            "access_token_expires_in": access_expires_ts,
            "refresh_token": new_refresh,
            "refresh_token_expires_in": refresh_expires_ts,
        }
        mock_requests_post.return_value = response

        # Act
        result = session_manager.attempt_session_refresh(refresh_token)

        # Assert
        assert result is True
        mock_requests_post.assert_called_once_with(
            url=REFRESH_URL,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {refresh_token}",
            },
            timeout=DEFAULT_TIMEOUT,
        )
        # Verify store_token was called correctly
        mock_keyring.set_password.assert_has_calls(
            [
                call(KEYRING_SERVICE, "access_token", new_access),
                call(
                    KEYRING_SERVICE, "access_token_expire_time", str(access_expires_ts)
                ),
                call(KEYRING_SERVICE, "refresh_token", new_refresh),
                call(
                    KEYRING_SERVICE,
                    "refresh_token_expire_time",
                    str(refresh_expires_ts),
                ),
            ],
            any_order=False,
        )

    def test_attempt_session_refresh_no_refresh_token(self, session_manager):
        # Arrange: refresh_token is None or empty string
        # Act & Assert
        with pytest.raises(ValueError, match="No refresh token available"):
            session_manager.attempt_session_refresh(None)
        with pytest.raises(ValueError, match="No refresh token available"):
            session_manager.attempt_session_refresh("")

    def test_attempt_session_refresh_api_failure(
        self, session_manager, mock_requests_post
    ):
        # Arrange
        refresh_token = "valid_refresh_token"
        response = MagicMock()
        response.status_code = 401
        response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "401 Client Error"
        )
        mock_requests_post.return_value = response

        # Act & Assert
        with pytest.raises(
            Exception,
            match="Failed to communicate with authentication server for refresh.",
        ):
            session_manager.attempt_session_refresh(refresh_token)
        assert session_manager.access_token is None

    def test_attempt_session_refresh_network_error(
        self, session_manager, mock_requests_post
    ):
        # Arrange
        refresh_token = "valid_refresh_token"
        mock_requests_post.side_effect = requests.exceptions.Timeout(
            "Connection timed out"
        )

        # Act & Assert
        with pytest.raises(
            Exception, match="Failed to communicate with authentication server"
        ):
            session_manager.attempt_session_refresh(refresh_token)
        # Ensure tokens are cleared on failure
        assert session_manager.access_token is None

    def test_attempt_session_refresh_missing_access_token_in_response(
        self, session_manager, mock_requests_post
    ):
        # Arrange
        refresh_token = "valid_refresh_token"
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {
            "message": "Success but no token"
        }  # Missing access_token
        mock_requests_post.return_value = response

        # Act & Assert
        with pytest.raises(
            ValueError, match="Refresh response did not contain an access token"
        ):
            session_manager.attempt_session_refresh(refresh_token)
        # Ensure tokens are cleared on failure
        assert session_manager.access_token is None

    def test_attempt_session_refresh_status_code_failure(
        self, session_manager, mock_requests_post
    ):
        # Arrange
        refresh_token = "valid_refresh_token"
        response = MagicMock()
        response.status_code = 404
        response.json.return_value = {"message": "Resource not found."}
        mock_requests_post.return_value = response

        # Act & Assert
        with pytest.raises(
            Exception,
            match=f"Failed to renew JWT access_token. Status: {response.status_code}",
        ):
            session_manager.attempt_session_refresh(refresh_token)
        assert session_manager.access_token is None

    # --- Test ensure_session_valid ---
    @patch.object(SessionManager, "check_expiration", return_value=False)
    @patch.object(SessionManager, "attempt_session_refresh")
    def test_ensure_session_valid_token_not_expired(
        self, mock_refresh, mock_check_exp, session_manager
    ):
        # Arrange (check_expiration returns False)

        # Act
        result = session_manager.ensure_session_valid()

        # Assert
        assert result is True
        mock_check_exp.assert_called_once()
        mock_refresh.assert_not_called()

    @patch.object(SessionManager, "check_expiration", return_value=True)
    @patch.object(SessionManager, "attempt_session_refresh", return_value=True)
    def test_ensure_session_valid_token_expired_refresh_success(
        self, mock_refresh, mock_check_exp, session_manager
    ):
        # Arrange
        session_manager.refresh_token = (
            "some_refresh_token"  # Need a refresh token to attempt
        )

        # Act
        result = session_manager.ensure_session_valid()

        # Assert
        assert result is True  # Should still indicate success overall if refresh worked
        mock_check_exp.assert_called_once()
        mock_refresh.assert_called_once_with(session_manager.refresh_token)

    @patch.object(SessionManager, "check_expiration", return_value=True)
    @patch.object(
        SessionManager,
        "attempt_session_refresh",
        side_effect=Exception("Refresh failed"),
    )
    def test_ensure_session_valid_token_expired_refresh_failure(
        self, mock_refresh, mock_check_exp, session_manager
    ):
        # Arrange
        session_manager.refresh_token = "some_refresh_token"

        # Act & Assert
        with pytest.raises(
            ConnectionAbortedError, match="Session refresh failed. Please log in again."
        ):
            session_manager.ensure_session_valid()

        mock_check_exp.assert_called_once()
        mock_refresh.assert_called_once_with(session_manager.refresh_token)

    # --- Test get_authenticated_headers ---
    @patch.object(SessionManager, "ensure_session_valid", return_value=True)
    @patch.object(
        SessionManager,
        "_get_current_auth_header",
        return_value={"Authorization": "Bearer valid_token"},
    )
    def test_get_authenticated_headers_success(
        self, mock_get_auth_header, mock_ensure_valid, session_manager
    ):
        # Arrange

        # Act
        headers = session_manager.get_authenticated_headers()

        # Assert
        mock_ensure_valid.assert_called_once()
        mock_get_auth_header.assert_called_once()
        assert headers == {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer valid_token",
        }

    @patch.object(
        SessionManager,
        "ensure_session_valid",
        side_effect=ConnectionAbortedError("Refresh failed"),
    )
    def test_get_authenticated_headers_refresh_fails(
        self, mock_ensure_valid, session_manager
    ):
        # Arrange

        # Act & Assert
        with pytest.raises(ConnectionAbortedError, match="Refresh failed"):
            session_manager.get_authenticated_headers()
        mock_ensure_valid.assert_called_once()

    @patch.object(SessionManager, "ensure_session_valid", return_value=True)
    @patch.object(
        SessionManager, "_get_current_auth_header", return_value={}
    )  # Simulate token got cleared somehow
    @patch.object(
        SessionManager, "clear_tokens"
    )  # Mock clear_tokens as it's called internally
    @patch("src.services.session_manager.logger", autospec=True)
    def test_get_authenticated_headers_no_auth_header_after_check(
        self,
        mock_logger,
        mock_clear,
        mock_get_auth_header,
        mock_ensure_valid,
        session_manager,
    ):
        # Arrange

        # Act & Assert
        with pytest.raises(
            ConnectionAbortedError,
            match="Authentication failed. No valid token available.",
        ):
            session_manager.get_authenticated_headers()

        mock_ensure_valid.assert_called_once()
        mock_get_auth_header.assert_called_once()
        mock_logger.error.assert_called_once_with(
            "Failed to get auth header even after session check."
        )
        mock_clear.assert_called_once()

    # --- Login Tests ---
    @patch("src.services.session_manager.keyring.set_password")
    @patch("src.services.session_manager.datetime", wraps=datetime)
    def test_login_success(
        self,
        mock_datetime,
        mock_keyring_set_password,
        session_manager,
        mock_requests_post,
    ):
        # Arrange
        mock_now = datetime.now(timezone.utc)
        mock_datetime.now.return_value = mock_now

        access_token = "test_token"
        refresh_token = "test_refresh_token"
        access_expires_ts = int(mock_now.timestamp()) + 3600
        refresh_expires_ts = int(mock_now.timestamp()) + 86400

        response = MagicMock()
        response.status_code = 201
        response.json.return_value = {
            "access_token": access_token,
            "access_token_expires_in": access_expires_ts,
            "refresh_token": refresh_token,
            "refresh_token_expires_in": refresh_expires_ts,
        }
        mock_requests_post.return_value = response
        username = "test_user"
        password = "test_password"

        # Act
        result = session_manager.login(username, password)

        # Assert
        mock_requests_post.assert_called_once_with(
            url=LOGIN_URL,
            json={"username": username, "password": password},
            headers=session_manager.base_headers,
            timeout=DEFAULT_TIMEOUT,
        )
        # Check that store_token was implicitly called via keyring mock
        mock_keyring_set_password.assert_has_calls(
            [
                call(KEYRING_SERVICE, "access_token", access_token),
                call(
                    KEYRING_SERVICE, "access_token_expire_time", str(access_expires_ts)
                ),
                call(KEYRING_SERVICE, "refresh_token", refresh_token),
                call(
                    KEYRING_SERVICE,
                    "refresh_token_expire_time",
                    str(refresh_expires_ts),
                ),
            ],
            any_order=False,
        )
        assert (
            result == response.json.return_value
        )  # Return value should be the full JSON
        assert (
            session_manager.access_token == access_token
        )  # Check internal state update
        assert session_manager.refresh_token == refresh_token

    @patch("src.services.session_manager.keyring.set_password")
    def test_login_failure_invalid_credentials(
        self, mock_keyring_set_password, session_manager, mock_requests_post
    ):
        # Arrange
        response = MagicMock()
        response.status_code = 401
        response.json.return_value = {"error": "Invalid Credentials"}
        mock_requests_post.return_value = response
        username = "invalid_user"
        password = "invalid_password"

        # Act
        result = session_manager.login(username, password)

        # Assert
        mock_requests_post.assert_called_once_with(
            url=LOGIN_URL,
            json={"username": username, "password": password},
            headers=session_manager.base_headers,
            timeout=DEFAULT_TIMEOUT,
        )
        assert result == {"error": "Invalid Credentials"}
        mock_keyring_set_password.assert_not_called()
        assert session_manager.access_token is None

    @patch("src.services.session_manager.keyring.set_password")
    def test_login_failure_server_error(
        self, mock_keyring_set_password, session_manager, mock_requests_post
    ):
        # Arrange
        response = MagicMock()
        response.status_code = 500
        response.json.return_value = {"error": "Internal Server Error"}
        mock_requests_post.return_value = response
        username = "test_user"
        password = "test_password"

        # Act
        result = session_manager.login(username, password)

        # Assert
        mock_requests_post.assert_called_once_with(
            url=LOGIN_URL,
            json={"username": username, "password": password},
            headers=session_manager.base_headers,
            timeout=DEFAULT_TIMEOUT,
        )
        assert result == {"error": "Internal Server Error"}
        mock_keyring_set_password.assert_not_called()
        assert session_manager.access_token is None

    @patch("src.services.session_manager.keyring.set_password")
    def test_login_network_error(
        self, mock_keyring_set_password, session_manager, mock_requests_post
    ):
        # Arrange
        mock_requests_post.side_effect = requests.exceptions.Timeout(
            "Connection timed out"
        )
        username = "test_user"
        password = "test_password"

        # Act & Assert
        # Login doesn't explicitly handle network errors, it lets requests raise them
        with pytest.raises(requests.exceptions.Timeout):
            session_manager.login(username, password)

        mock_keyring_set_password.assert_not_called()
        assert session_manager.access_token is None

    # --- Logout Tests ---
    @patch.object(SessionManager, "get_authenticated_headers")
    @patch.object(SessionManager, "clear_tokens")
    @patch("src.services.session_manager.logger", autospec=True)
    def test_logout_success(
        self,
        mock_logger,
        mock_clear_tokens,
        mock_get_headers,
        session_manager,
        mock_requests_delete,
    ):
        # Arrange
        # Assume user is logged in (mocks will handle token presence)
        auth_headers = {
            **session_manager.base_headers,
            "Authorization": "Bearer test_token",
        }
        mock_get_headers.return_value = auth_headers

        response = MagicMock()
        response.status_code = 204  # Success, no content
        mock_requests_delete.return_value = response

        # Act
        session_manager.logout()

        # Assert
        mock_get_headers.assert_called_once()  # Ensure it tried to get headers
        mock_requests_delete.assert_called_once_with(
            url=LOGOUT_URL,
            headers=auth_headers,  # Verify correct headers were used
            timeout=DEFAULT_TIMEOUT,
        )
        mock_clear_tokens.assert_called_once()  # Verify tokens were cleared on success
        mock_logger.info.assert_any_call("Logging out user.")
        mock_logger.info.assert_any_call(
            "User logged out successfully. Clearing local tokens."
        )

    @patch.object(SessionManager, "get_authenticated_headers")
    def test_logout_failure_api_error(
        self, mock_get_headers, session_manager, mock_requests_delete
    ):
        # Arrange
        auth_headers = {
            **session_manager.base_headers,
            "Authorization": "Bearer test_token",
        }
        mock_get_headers.return_value = auth_headers

        response = MagicMock()
        response.status_code = 400
        response.json.return_value = {"error": "Bad Request"}
        mock_requests_delete.return_value = response

        # Act & Assert
        with pytest.raises(Exception, match="Failed to logout user."):
            session_manager.logout()

        mock_get_headers.assert_called_once()
        mock_requests_delete.assert_called_once_with(
            url=LOGOUT_URL,
            headers=auth_headers,
            timeout=DEFAULT_TIMEOUT,
        )

    @patch.object(SessionManager, "get_authenticated_headers")
    def test_logout_network_error(
        self, mock_get_headers, session_manager, mock_requests_delete
    ):
        # Arrange
        auth_headers = {
            **session_manager.base_headers,
            "Authorization": "Bearer test_token",
        }
        mock_get_headers.return_value = auth_headers
        mock_requests_delete.side_effect = requests.exceptions.ConnectionError(
            "Network issue"
        )

        # Act & Assert
        with pytest.raises(requests.exceptions.ConnectionError):
            session_manager.logout()

        mock_get_headers.assert_called_once()
        mock_requests_delete.assert_called_once_with(
            url=LOGOUT_URL,
            headers=auth_headers,
            timeout=DEFAULT_TIMEOUT,
        )

    @patch.object(
        SessionManager,
        "ensure_session_valid",
        side_effect=ConnectionAbortedError("Session invalid"),
    )
    def test_logout_session_invalid(
        self, mock_ensure_valid, session_manager, mock_requests_delete
    ):
        # Arrange: ensure_session_valid fails

        # Act & Assert
        with pytest.raises(ConnectionAbortedError, match="Session invalid"):
            session_manager.logout()  # The error comes from get_authenticated_headers

        mock_ensure_valid.assert_called_once()
        mock_requests_delete.assert_not_called()
