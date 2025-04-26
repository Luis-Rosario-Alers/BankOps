from unittest.mock import MagicMock, patch

import pytest
from requests import Response
from requests.exceptions import RequestException

from src.services.api_client_service import APIClient, APIClientError, SessionManager

BASE_URL = "http://127.0.0.1:5000/api/v1/"
USERS_URL = "users"
CURRENT_USER_URL = "users/current"
TRANSACTIONS_URL = "transactions"
ACCOUNTS_URL = "accounts"
DEFAULT_TIMEOUT = 5


class TestAPIClient:
    @pytest.fixture
    def api_client(self):
        client = APIClient(base_url=BASE_URL, timeout=DEFAULT_TIMEOUT)
        return client

    @pytest.fixture
    def mock_make_request(self):
        # Patch the internal _make_request method
        with patch.object(APIClient, "_make_request", autospec=True) as mock_method:
            yield mock_method

    @patch("src.services.api_client_service.requests.request")
    @patch.object(
        SessionManager,
        "get_authenticated_headers",
        return_value={"Authorization": "Bearer test_token"},
    )
    def test_make_request_authenticated_successful(
        self, mock_get_headers, mock_request, api_client
    ):
        # Arrange
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"json_data": "test_json"}
        mock_request.return_value = mock_response

        endpoint = "test_endpoint"
        method = "GET"
        authenticated = True
        expected_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer test_token",
        }
        expected_params = {"param1": "value1"}
        expected_timeout = DEFAULT_TIMEOUT

        # Act
        api_client._make_request(
            method, endpoint, authenticated, expected_status=200, params=expected_params
        )

        # Assert
        mock_request.assert_called_once_with(
            method=method,
            url=f"{BASE_URL}{endpoint}",
            headers=expected_headers,
            timeout=expected_timeout,
            params=expected_params,
        )

    @patch("src.services.api_client_service.requests.request")
    @patch.object(
        SessionManager,
        "get_authenticated_headers",
        side_effect=APIClientError("Failed to get authenticated headers"),
    )
    def test_make_request_authenticated_headers_failed(
        self, mock_get_headers, mock_request, api_client
    ):
        # Arrange
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        endpoint = "test_endpoint"
        method = "GET"
        authenticated = True
        expected_params = {"param1": "value1"}

        # Act & Assert
        with pytest.raises(APIClientError, match="Failed to get authenticated headers"):
            api_client._make_request(
                method,
                endpoint,
                authenticated,
                expected_status=200,
                params=expected_params,
            )

    @patch(
        "src.services.api_client_service.requests.request",
        side_effect=RequestException("Request exception"),
    )
    @patch.object(SessionManager, "get_authenticated_headers")
    def test_make_request_requestException(
        self, mock_get_headers, mock_request, api_client
    ):
        # Arrange
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        endpoint = "test_endpoint"
        method = "GET"
        authenticated = True
        expected_params = {"param1": "value1"}

        # Act & Assert
        with pytest.raises(APIClientError):
            api_client._make_request(
                method,
                endpoint,
                authenticated,
                expected_status=200,
                params=expected_params,
            )

    @patch("src.services.api_client_service.requests.request")
    @patch.object(SessionManager, "get_authenticated_headers")
    def test_make_request_status_code_check_failure(
        self, mock_get_headers, mock_request, api_client
    ):
        # Arrange
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 400  # Different from the expected status code
        mock_request.return_value = mock_response

        endpoint = "test_endpoint"
        method = "GET"
        authenticated = True
        expected_params = {"param1": "value1"}
        expected_status = 200

        # Act & Assert
        with pytest.raises(APIClientError):
            api_client._make_request(
                method,
                endpoint,
                authenticated,
                expected_status=expected_status,
                params=expected_params,
            )

    @patch(
        "src.services.api_client_service.requests.request",
        side_effect=APIClientError("Random Error"),
    )
    @patch.object(SessionManager, "get_authenticated_headers")
    def test_make_request_handle_api_client_error(
        self, mock_get_headers, mock_request, api_client
    ):
        # Arrange
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        endpoint = "test_endpoint"
        method = "GET"
        authenticated = True
        expected_params = {"param1": "value1"}
        expected_status = 200

        # Act & Assert
        with pytest.raises(APIClientError):
            api_client._make_request(
                method,
                endpoint,
                authenticated,
                expected_status=expected_status,
                params=expected_params,
            )

    # --- Retrieve User Info Tests ---
    @patch.object(
        SessionManager,
        "get_authenticated_headers",
        return_value={"Authorization": "Bearer test_token"},
    )
    def test_retrieve_user_info_success(
        self, mock_get_headers, api_client, mock_make_request
    ):
        # Arrange
        user_profile_response = MagicMock(spec=Response)
        user_profile_response.status_code = 200
        user_profile_response.json.return_value = {
            "user": {"id": "123", "name": "Test User"}
        }

        user_accounts_response = MagicMock(spec=Response)
        user_accounts_response.status_code = 200
        user_accounts_response.json.return_value = {
            "accounts": ["account1", "account2"]
        }

        mock_make_request.side_effect = [user_profile_response, user_accounts_response]

        # Act
        result = api_client.retrieve_user_info()

        # Assert
        assert mock_make_request.call_count == 2
        mock_make_request.assert_any_call(
            api_client,
            method="GET",
            endpoint=CURRENT_USER_URL,
            authenticated=True,
            expected_status=200,
        )
        mock_make_request.assert_any_call(
            api_client,
            method="GET",
            endpoint=f"{USERS_URL}/123/accounts",
            authenticated=True,
            expected_status=200,
        )
        assert result == {
            "user_profile": {"id": "123", "name": "Test User"},
            "user_accounts": {"accounts": ["account1", "account2"]},
        }

    @patch.object(
        SessionManager,
        "get_authenticated_headers",
        return_value={"Authorization": "Bearer test_token"},
    )
    def test_retrieve_user_info_failure_profile_request_api_error(
        self, mock_get_headers, api_client, mock_make_request
    ):
        # Arrange
        mock_make_request.side_effect = APIClientError("Failed profile request")

        # Act & Assert
        with pytest.raises(
            APIClientError,
            match="Failed to retrieve complete user information: "
            "Failed profile request",
        ):
            api_client.retrieve_user_info()

        mock_make_request.assert_called_once_with(
            api_client,
            method="GET",
            endpoint=CURRENT_USER_URL,
            authenticated=True,
            expected_status=200,
        )

    @patch.object(
        SessionManager,
        "get_authenticated_headers",
        return_value={"Authorization": "Bearer test_token"},
    )
    def test_retrieve_user_info_failure_profile_malformed(
        self, mock_get_headers, api_client, mock_make_request
    ):
        # Arrange
        user_profile_response = MagicMock(spec=Response)
        user_profile_response.status_code = 200
        user_profile_response.json.return_value = {"not_user": {"id": "123"}}
        mock_make_request.return_value = user_profile_response

        # Act & Assert
        with pytest.raises(
            APIClientError,
            match="Failed to retrieve complete user information: "
            "User profile data is missing or malformed",
        ):
            api_client.retrieve_user_info()

        mock_make_request.assert_called_once_with(
            api_client,
            method="GET",
            endpoint=CURRENT_USER_URL,
            authenticated=True,
            expected_status=200,
        )

    @patch.object(
        SessionManager,
        "get_authenticated_headers",
        return_value={"Authorization": "Bearer test_token"},
    )
    def test_retrieve_user_info_failure_accounts_request(
        self, mock_get_headers, api_client, mock_make_request
    ):
        # Arrange
        user_profile_response = MagicMock(spec=Response)
        user_profile_response.status_code = 200
        user_profile_response.json.return_value = {
            "user": {"id": "123", "name": "Test User"}
        }

        mock_make_request.side_effect = [
            user_profile_response,
            APIClientError("Failed accounts request"),
        ]

        # Act & Assert
        with pytest.raises(
            APIClientError,
            match="Failed to retrieve complete user information: "
            "Failed accounts request",
        ):
            api_client.retrieve_user_info()

        # Assert
        assert mock_make_request.call_count == 2
        mock_make_request.assert_any_call(
            api_client,
            method="GET",
            endpoint=CURRENT_USER_URL,
            authenticated=True,
            expected_status=200,
        )
        mock_make_request.assert_any_call(
            api_client,
            method="GET",
            endpoint=f"{USERS_URL}/123/accounts",
            authenticated=True,
            expected_status=200,
        )

    # --- Create User Test ---
    def test_create_user_success(self, api_client, mock_make_request):
        # Arrange
        response = MagicMock(spec=Response)
        response.status_code = 201
        response.json.return_value = {"id": "123", "email": "test@test.com"}
        mock_make_request.return_value = response

        email = "test@test.com"
        username = "test_user"
        password = "password"
        expected_payload = {"email": email, "username": username, "password": password}

        # Act
        result = api_client.create_user(email, username, password)

        # Assert
        mock_make_request.assert_called_once_with(
            api_client,
            method="POST",
            endpoint=USERS_URL,
            authenticated=False,
            json=expected_payload,
            expected_status=201,
        )
        assert result == {"id": "123", "email": "test@test.com"}

    def test_create_user_failure(self, api_client, mock_make_request):
        # Arrange
        mock_make_request.side_effect = APIClientError("Creation failed")
        email = "test@test.com"
        username = "test_user"
        password = "password"
        expected_payload = {"email": email, "username": username, "password": password}

        # Act & Assert
        with pytest.raises(
            APIClientError, match="Failed to create user: Creation failed"
        ):
            api_client.create_user(email, username, password)

        # Assert
        mock_make_request.assert_called_once_with(
            api_client,
            method="POST",
            endpoint=USERS_URL,
            authenticated=False,
            json=expected_payload,
            expected_status=201,
        )

    # --- Retrieve User Transactions Tests ---
    @patch.object(
        SessionManager,
        "get_authenticated_headers",
        return_value={"Authorization": "Bearer test_token"},
    )
    def test_retrieve_user_transactions_default_params(
        self, mock_get_headers, api_client, mock_make_request
    ):
        # Arrange
        response = MagicMock(spec=Response)
        response.status_code = 200
        response.json.return_value = {"transactions": [{"id": 1}, {"id": 2}]}
        mock_make_request.return_value = response
        expected_params = {"limit": 30, "offset": 0}

        # Act
        result = api_client.retrieve_user_transactions()

        # Assert
        mock_make_request.assert_called_once_with(
            api_client,
            method="GET",
            endpoint=TRANSACTIONS_URL,
            authenticated=True,
            params=expected_params,
            expected_status=200,
        )
        assert result == {"transactions": [{"id": 1}, {"id": 2}]}

    @patch.object(
        SessionManager,
        "get_authenticated_headers",
        return_value={"Authorization": "Bearer test_token"},
    )
    def test_retrieve_user_transactions_with_params(
        self, mock_get_headers, api_client, mock_make_request
    ):
        # Arrange
        response = MagicMock(spec=Response)
        response.status_code = 200
        response.json.return_value = {"transactions": [{"id": 3, "type": "DEBIT"}]}
        mock_make_request.return_value = response

        limit = 10
        offset = 5
        transaction_type = "DEBIT"
        account_number = "ACC123"

        expected_params = {
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
        mock_make_request.assert_called_once_with(
            api_client,
            method="GET",
            endpoint=TRANSACTIONS_URL,
            authenticated=True,
            params=expected_params,
            expected_status=200,
        )
        assert result == {"transactions": [{"id": 3, "type": "DEBIT"}]}

    @patch.object(
        SessionManager,
        "get_authenticated_headers",
        return_value={"Authorization": "Bearer test_token"},
    )
    def test_retrieve_user_transactions_failure(
        self, mock_get_headers, api_client, mock_make_request
    ):
        # Arrange
        mock_make_request.side_effect = APIClientError("Failed fetch")

        # Act & Assert
        with pytest.raises(
            APIClientError, match="Failed to retrieve user transactions: Failed fetch"
        ):
            api_client.retrieve_user_transactions()

        # Assert
        mock_make_request.assert_called_once_with(
            api_client,
            method="GET",
            endpoint=TRANSACTIONS_URL,
            authenticated=True,
            params={"limit": 30, "offset": 0},
            expected_status=200,
        )

    # --- Get Account Details Tests ---
    @patch.object(
        SessionManager,
        "get_authenticated_headers",
        return_value={"Authorization": "Bearer test_token"},
    )
    def test_get_account_details_no_filter(
        self, mock_get_headers, api_client, mock_make_request
    ):
        # Arrange
        account_number = "12345"
        response = MagicMock(spec=Response)
        response.status_code = 200
        full_account_data = {
            "account": {"id": account_number, "balance": 1000, "currency": "USD"}
        }
        response.json.return_value = full_account_data
        mock_make_request.return_value = response
        expected_endpoint = f"{ACCOUNTS_URL}/{account_number}"

        # Act
        result = api_client.get_account_details(account_number)

        # Assert
        mock_make_request.assert_called_once_with(
            api_client,
            method="GET",
            endpoint=expected_endpoint,
            authenticated=True,
            expected_status=200,
        )
        assert result == {"id": account_number, "balance": 1000, "currency": "USD"}

    @patch.object(
        SessionManager,
        "get_authenticated_headers",
        return_value={"Authorization": "Bearer test_token"},
    )
    def test_get_account_details_with_filter(
        self, mock_get_headers, api_client, mock_make_request
    ):
        # Arrange
        account_number = "12345"
        response = MagicMock(spec=Response)
        response.status_code = 200
        full_account_data = {
            "account": {
                "id": account_number,
                "balance": 1000,
                "currency": "USD",
                "owner": "Test User",
                "status": "ACTIVE",
            }
        }
        response.json.return_value = full_account_data
        mock_make_request.return_value = response
        expected_endpoint = f"{ACCOUNTS_URL}/{account_number}"

        # Act
        result = api_client.get_account_details(
            account_number, "balance", "owner", "type"
        )  # 'type' is not in response

        # Assert
        mock_make_request.assert_called_once_with(
            api_client,
            method="GET",
            endpoint=expected_endpoint,
            authenticated=True,
            expected_status=200,
        )
        assert result == {"balance": 1000, "owner": "Test User"}

    @patch.object(
        SessionManager,
        "get_authenticated_headers",
        return_value={"Authorization": "Bearer test_token"},
    )
    def test_get_account_details_failure_api_error(
        self, mock_get_headers, api_client, mock_make_request
    ):
        # Arrange
        account_number = "99999"
        mock_make_request.side_effect = APIClientError("Account not found")
        expected_endpoint = f"{ACCOUNTS_URL}/{account_number}"

        # Act & Assert
        with pytest.raises(
            APIClientError,
            match=f"Failed to retrieve or filter account "
            f"details for {account_number}: Account not found",
        ):
            api_client.get_account_details(account_number)

        # Assert
        mock_make_request.assert_called_once_with(
            api_client,
            method="GET",
            endpoint=expected_endpoint,
            authenticated=True,
            expected_status=200,
        )

    @patch.object(
        SessionManager,
        "get_authenticated_headers",
        return_value={"Authorization": "Bearer test_token"},
    )
    def test_get_account_details_malformed_response(
        self, mock_get_headers, api_client, mock_make_request
    ):
        # Arrange
        account_number = "12345"
        response = MagicMock(spec=Response)
        response.status_code = 200
        response.json.return_value = {
            "message": "Data retrieved"
        }  # Missing 'account' key
        mock_make_request.return_value = response
        expected_endpoint = f"{ACCOUNTS_URL}/{account_number}"

        # Act & Assert
        with pytest.raises(
            APIClientError,
            match=f"Failed to retrieve or filter account details for {account_number}: "
            f"Account data is missing or not a dictionary",
        ):
            api_client.get_account_details(account_number)

        # Assert
        mock_make_request.assert_called_once_with(
            api_client,
            method="GET",
            endpoint=expected_endpoint,
            authenticated=True,
            expected_status=200,
        )
