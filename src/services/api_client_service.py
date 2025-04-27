from typing import Any, Dict, Optional

import requests
from requests import Response
from requests.exceptions import RequestException

from src.services.session_manager import SessionManager


class APIClientError(Exception):
    pass


class APIClient:
    """
    Service class providing methods to interact with the backend API.
    Handles session management for authenticated requests using SessionManager.
    """

    def __init__(
        self, base_url: str = "http://127.0.0.1:5000/api/v1/", timeout: int = 5
    ):
        """
        Initializes the API client.

        :param base_url: The base URL for the API endpoints.
        :param timeout: Default request timeout in seconds.
        """
        self.base_url = base_url.rstrip("/") + "/"
        self.base_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.session_manager = SessionManager()
        self.timeout = timeout

    def _make_request(
        self,
        method: str,
        endpoint: str,
        authenticated: bool = False,
        expected_status: Optional[int] = None,
        **kwargs: Any,
    ) -> Response:
        """
        Internal helper method to execute HTTP requests to the API.

        :param method: HTTP method ('GET', 'POST', etc.).
        :param endpoint: API endpoint path relative to base_url.
        :param authenticated: If True, add authentication headers.
        :param expected_status: If set, verify the response status code.
        :param kwargs: Additional arguments for requests.request.
        :return: The request Response object.
        :raises APIClientError: If authentication fails, the request fails,
                                 or the status code doesn't match expected_status.
        """
        url = f"{self.base_url}{endpoint.lstrip('/')}"
        headers = self.base_headers.copy()

        if authenticated:
            try:
                auth_headers = self.session_manager.get_authenticated_headers()
                headers.update(auth_headers)
            except Exception as e:
                raise APIClientError(
                    f"Authentication failed before request: {e}"
                ) from e

        try:
            response = requests.request(
                method=method, url=url, headers=headers, timeout=self.timeout, **kwargs
            )
            response.raise_for_status()

            if expected_status is not None and response.status_code != expected_status:
                raise APIClientError(
                    f"Request to {endpoint} returned status {response.status_code}, "
                    f"but expected {expected_status}."
                )

            return response
        except RequestException as e:
            raise APIClientError(
                f"API request failed for {method} {endpoint}: {e}"
            ) from e
        except APIClientError:
            raise
        except Exception as e:
            raise APIClientError(
                f"An unexpected error occurred during the request to {endpoint}: {e}"
            ) from e

    def retrieve_user_info(self) -> Dict[str, Any]:
        """
        Retrieves the current user's profile and associated account information.

        :return: A dictionary with 'user_profile' and 'user_accounts'.
        :raises APIClientError: If fetching fails or data is malformed.
        """
        try:
            user_profile_response = self._make_request(
                method="GET",
                endpoint="users/current",
                authenticated=True,
                expected_status=200,
            )
            user_profile_data = user_profile_response.json()

            user_info = user_profile_data.get("user")
            if not isinstance(user_info, dict) or "id" not in user_info:
                raise APIClientError(
                    "User profile data is missing or malformed in response."
                )

            user_id = user_info["id"]

            user_accounts_response = self._make_request(
                method="GET",
                endpoint=f"users/{user_id}/accounts",
                authenticated=True,
                expected_status=200,
            )
            user_accounts_data = user_accounts_response.json()

            return {
                "user_profile": user_info,
                "user_accounts": user_accounts_data,
            }
        except (APIClientError, ValueError, KeyError) as e:
            raise APIClientError(
                f"Failed to retrieve complete user information: {e}"
            ) from e

    def create_user(self, email: str, username: str, password: str) -> Dict[str, Any]:
        """
        Sends a request to create a new user account.

        :param email: User's email address.
        :param username: Desired username.
        :param password: User's password.
        :return: The API response JSON upon successful creation.
        :raises APIClientError: If user creation fails.
        """
        payload = {"email": email, "username": username, "password": password}
        try:
            response = self._make_request(
                method="POST",
                endpoint="users",
                authenticated=False,
                json=payload,
                expected_status=201,
            )
            return response.json()
        except (APIClientError, ValueError) as e:
            raise APIClientError(f"Failed to create user: {e}") from e

    def retrieve_user_transactions(
        self,
        limit: int = 30,
        offset: int = 0,
        transaction_type: Optional[str] = None,
        account_number: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retrieves transactions for the authenticated user, with optional filters.

        :param limit: Max number of transactions.
        :param offset: Offset for pagination.
        :param transaction_type: Filter by type (e.g., 'DEPOSIT').
        :param account_number: Filter by account number.
        :return: API response JSON with transaction data.
        :raises APIClientError: If retrieving transactions fails.
        """
        params: Dict[str, Any] = {
            "limit": limit,
            "offset": offset,
        }
        if transaction_type:
            params["transaction_type"] = transaction_type
        if account_number:
            params["account_number"] = account_number

        try:
            response = self._make_request(
                method="GET",
                endpoint="transactions",
                authenticated=True,
                params=params,
                expected_status=200,
            )
            return response.json()
        except (APIClientError, ValueError) as e:
            raise APIClientError(f"Failed to retrieve user transactions: {e}") from e

    def get_account_details(
        self, account_number: str, *filter_keys: str
    ) -> Dict[str, Any]:
        """
        Fetches details for a specific account, optionally filtering returned fields.

        :param account_number: Account number to query.
        :param filter_keys: Optional field names to include in the result.
        If empty, return all fields.
        :return: Dictionary containing account details (potentially filtered).
        :raises APIClientError: If fetching fails or data is malformed.
        """
        try:
            response = self._make_request(
                method="GET",
                endpoint=f"accounts/{account_number}",
                authenticated=True,
                expected_status=200,
            )
            data = response.json()
            account_data = data.get("account")

            if not isinstance(account_data, dict):
                raise APIClientError(
                    "Account data is missing or not a dictionary in the response."
                )

            if filter_keys:
                # Return only the requested keys that exist in the account data
                return {
                    key: account_data[key] for key in filter_keys if key in account_data
                }
            else:
                # Return all account data if no specific keys requested
                return account_data

        except (APIClientError, ValueError, KeyError) as e:
            raise APIClientError(
                f"Failed to retrieve or filter "
                f"account details for {account_number}: {e}"
            ) from e
