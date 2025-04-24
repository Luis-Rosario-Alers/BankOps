from unittest.mock import MagicMock, patch

import pytest
import requests

from src.services.api_client_service import APIClient

BASE_URL = " http://127.0.0.1:5000/api/v1/"
LOGIN_URL = f"{BASE_URL}auth/sessions/users"
USERS_URL = f"{BASE_URL}users"
CURRENT_USER_URL = f"{USERS_URL}/current"
TRANSACTIONS_URL = f"{BASE_URL}transactions"
ACCOUNTS_URL = f"{BASE_URL}accounts"
DEFAULT_TIMEOUT = 5


class TestAPIClient:
    @pytest.fixture
    def api_client(self):
        client = APIClient()
        client.base_url = BASE_URL

        yield client

        client.token = None
        client.headers["Authorization"] = None

    # --- Mock Fixtures ---
    @pytest.fixture
    def mock_requests_post(self):
        with patch("src.services.api_client_service.requests.post") as mock_post:
            yield mock_post

    @pytest.fixture
    def mock_requests_get(self):
        with patch("src.services.api_client_service.requests.get") as mock_get:
            yield mock_get

    def set_authenticated_state(self, client, token="test_token"):
        """Helper to set the token and header for tests requiring auth."""
        client.token = token
        client.headers["Authorization"] = f"Bearer {token}"

    # --- Login Tests ---
    def test_login_success(self, api_client, mock_requests_post):
        # Arrange
        response = MagicMock()
        response.status_code = 201
        response.json.return_value = {"access_token": "test_token"}
        mock_requests_post.return_value = response
        username = "test_user"
        password = "test_password"

        # Act
        result = api_client.login(username, password)

        # Assert
        mock_requests_post.assert_called_once_with(
            url=LOGIN_URL,
            json={"username": username, "password": password},
            headers=api_client.headers,
            timeout=DEFAULT_TIMEOUT,
        )
        assert result == {"access_token": "test_token"}
        assert api_client.token == "test_token"
        assert api_client.headers["Authorization"] == "Bearer test_token"

    def test_login_failure_invalid_credentials(self, api_client, mock_requests_post):
        # Arrange
        response = MagicMock()
        response.status_code = 401
        response.json.return_value = {"error": "Invalid Credentials"}
        mock_requests_post.return_value = response
        username = "invalid_user"
        password = "invalid_password"

        # Act
        result = api_client.login(username, password)

        # Assert
        mock_requests_post.assert_called_once_with(
            url=LOGIN_URL,
            json={"username": username, "password": password},
            headers=api_client.headers,
            timeout=DEFAULT_TIMEOUT,
        )
        assert result == {"error": "Invalid Credentials"}
        assert api_client.token is None
        assert api_client.headers["Authorization"] is None

    def test_login_failure_server_error(self, api_client, mock_requests_post):
        # Arrange
        response = MagicMock()
        response.status_code = 500
        response.json.return_value = {"error": "Internal Server Error"}
        mock_requests_post.return_value = response
        username = "test_user"
        password = "test_password"

        # Act
        result = api_client.login(username, password)

        # Assert
        mock_requests_post.assert_called_once_with(
            url=LOGIN_URL,
            json={"username": username, "password": password},
            headers=api_client.headers,
            timeout=DEFAULT_TIMEOUT,
        )
        assert result == {"error": "Internal Server Error"}
        assert api_client.token is None
        assert api_client.headers["Authorization"] is None

    def test_login_network_error(self, api_client, mock_requests_post):
        # Arrange
        mock_requests_post.side_effect = requests.exceptions.Timeout(
            "Connection timed out"
        )
        username = "test_user"
        password = "test_password"

        # Act & Assert
        with pytest.raises(requests.exceptions.Timeout):
            api_client.login(username, password)

        assert api_client.token is None
        assert api_client.headers["Authorization"] is None

    # --- Retrieve User Info Tests ---
    def test_retrieve_user_info_success(self, api_client, mock_requests_get):
        # Arrange
        self.set_authenticated_state(api_client)  # Set auth state explicitly

        user_profile_response = MagicMock()
        user_profile_response.status_code = 200
        user_profile_response.json.return_value = {
            "user": {"id": "123", "name": "Test User"}
        }

        user_accounts_response = MagicMock()
        user_accounts_response.status_code = 200
        user_accounts_response.json.return_value = {
            "accounts": ["account1", "account2"]
        }

        mock_requests_get.side_effect = [user_profile_response, user_accounts_response]
        expected_headers = api_client.headers

        # Act
        result = api_client.retrieve_user_info()

        # Assert
        assert mock_requests_get.call_count == 2
        # Check first call (user profile)
        mock_requests_get.assert_any_call(
            url=CURRENT_USER_URL,
            headers=expected_headers,
            timeout=DEFAULT_TIMEOUT,
        )
        # Check second call (user accounts)
        mock_requests_get.assert_any_call(
            url=f"{USERS_URL}/123/accounts",
            headers=expected_headers,
            timeout=DEFAULT_TIMEOUT,
        )
        assert result == {
            "user_profile": {"id": "123", "name": "Test User"},
            "user_accounts": {"accounts": ["account1", "account2"]},
        }

    def test_retrieve_user_info_failure_profile_request(
        self, api_client, mock_requests_get
    ):
        # Arrange
        self.set_authenticated_state(api_client)
        user_profile_response = MagicMock()
        user_profile_response.status_code = 404
        mock_requests_get.return_value = user_profile_response
        expected_headers = api_client.headers

        # Act & Assert
        with pytest.raises(
            Exception, match="Failed to retrieve user information from server"
        ):
            api_client.retrieve_user_info()

        mock_requests_get.assert_called_once_with(
            url=CURRENT_USER_URL,
            headers=expected_headers,
            timeout=DEFAULT_TIMEOUT,
        )

    def test_retrieve_user_info_failure_accounts_request(
        self, api_client, mock_requests_get
    ):
        # Arrange
        self.set_authenticated_state(api_client)
        user_profile_response = MagicMock()
        user_profile_response.status_code = 200
        user_profile_response.json.return_value = {
            "user": {"id": "123", "name": "Test User"}
        }

        user_accounts_response = MagicMock()
        user_accounts_response.status_code = 500

        mock_requests_get.side_effect = [user_profile_response, user_accounts_response]
        expected_headers = api_client.headers

        # Act & Assert
        with pytest.raises(
            Exception, match="Failed to retrieve user information from server"
        ):
            api_client.retrieve_user_info()

        assert mock_requests_get.call_count == 2
        mock_requests_get.assert_any_call(
            url=CURRENT_USER_URL, headers=expected_headers, timeout=DEFAULT_TIMEOUT
        )
        mock_requests_get.assert_any_call(
            url=f"{USERS_URL}/123/accounts",
            headers=expected_headers,
            timeout=DEFAULT_TIMEOUT,
        )

    # --- Create User Test ---
    def test_create_user(self, api_client, mock_requests_post):
        # Arrange
        response = MagicMock()
        response.status_code = 201
        response.json.return_value = {"id": "123", "email": "test@test.com"}
        mock_requests_post.return_value = response
        email = "test@test.com"
        username = "test_user"
        password = "password"

        # Act
        result = api_client.create_user(email, username, password)

        # Assert
        # Use client's initial headers (no auth token expected)
        initial_headers = api_client.headers.copy()
        initial_headers["Authorization"] = None  # Ensure no auth token

        mock_requests_post.assert_called_once_with(
            url=USERS_URL,
            json={"email": email, "username": username, "password": password},
            headers=initial_headers,
            timeout=DEFAULT_TIMEOUT,
        )
        assert result == {"id": "123", "email": "test@test.com"}
        assert api_client.token is None

    # --- Retrieve User Transactions Tests ---
    def test_retrieve_user_transactions_default_params(
        self, api_client, mock_requests_get
    ):
        # Arrange
        self.set_authenticated_state(api_client)
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {"transactions": [{"id": 1}, {"id": 2}]}
        mock_requests_get.return_value = response
        expected_headers = api_client.headers

        # Expected JSON payload with defaults for None parameters
        expected_payload = {
            "limit": 30,
            "offset": 0,
            "transaction_type": None,
            "account_number": None,
        }

        # Act
        result = api_client.retrieve_user_transactions()  # Use defaults

        # Assert
        mock_requests_get.assert_called_once_with(
            url=TRANSACTIONS_URL,
            headers=expected_headers,
            timeout=DEFAULT_TIMEOUT,
            json=expected_payload,
        )
        assert result == {"transactions": [{"id": 1}, {"id": 2}]}

    def test_retrieve_user_transactions_with_params(
        self, api_client, mock_requests_get
    ):
        # Arrange
        self.set_authenticated_state(api_client)
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {"transactions": [{"id": 3, "type": "DEBIT"}]}
        mock_requests_get.return_value = response
        expected_headers = api_client.headers

        limit = 10
        offset = 5
        transaction_type = "DEBIT"
        account_number = "ACC123"

        # Expected JSON payload with specified parameters
        expected_payload = {
            "limit": limit,
            "offset": offset,
            "transaction_type": transaction_type,
            "account_number": account_number,
        }

        # Act
        result = api_client.retrieve_user_transactions(
            limit=limit,
            offset=offset,
            transaction_type=transaction_type,
            account_number=account_number,
        )

        # Assert
        mock_requests_get.assert_called_once_with(
            url=TRANSACTIONS_URL,
            headers=expected_headers,
            timeout=DEFAULT_TIMEOUT,
            json=expected_payload,
        )
        assert result == {"transactions": [{"id": 3, "type": "DEBIT"}]}

    # --- Get Account Details Tests ---
    def test_get_account_details_no_filter(self, api_client, mock_requests_get):
        # Arrange
        self.set_authenticated_state(api_client)
        account_number = "12345"
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {
            "account": {"id": account_number, "balance": 1000, "currency": "USD"}
        }
        mock_requests_get.return_value = response
        expected_headers = api_client.headers

        # Act
        result = api_client.get_account_details(account_number)

        # Assert
        mock_requests_get.assert_called_once_with(
            url=f"{ACCOUNTS_URL}/{account_number}",
            headers=expected_headers,
            timeout=DEFAULT_TIMEOUT,
        )
        assert result == {
            "account": {"id": "12345", "balance": 1000, "currency": "USD"}
        }

    def test_get_account_details_with_filter(self, api_client, mock_requests_get):
        # Arrange
        self.set_authenticated_state(api_client)
        account_number = "12345"
        response = MagicMock()
        response.status_code = 200
        full_account_data = {
            "account": {
                "id": account_number,
                "balance": 1000,
                "currency": "USD",
                "owner": "Test User",
            }
        }
        response.json.return_value = full_account_data
        mock_requests_get.return_value = response
        expected_headers = api_client.headers

        # Act - filter for 'balance' and 'owner'
        result = api_client.get_account_details(account_number, "balance", "owner")

        # Assert
        mock_requests_get.assert_called_once_with(
            url=f"{ACCOUNTS_URL}/{account_number}",
            headers=expected_headers,
            timeout=DEFAULT_TIMEOUT,
        )
        assert result == {"balance": 1000, "owner": "Test User"}

    def test_get_account_details_failure(self, api_client, mock_requests_get):
        # Arrange
        self.set_authenticated_state(api_client)
        account_number = "99999"  # Non-existent account
        response = MagicMock()
        response.status_code = 404
        response.json.return_value = {"error": "Account not found"}
        mock_requests_get.return_value = response
        expected_headers = api_client.headers

        # Act
        result = api_client.get_account_details(account_number)

        # Assert
        mock_requests_get.assert_called_once_with(
            url=f"{ACCOUNTS_URL}/{account_number}",
            headers=expected_headers,
            timeout=DEFAULT_TIMEOUT,
        )
        assert result == {"error": "Account not found"}
