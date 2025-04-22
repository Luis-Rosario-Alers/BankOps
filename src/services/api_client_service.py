import requests

from src import SingletonMeta


class APIClient(metaclass=SingletonMeta):
    """
    A service class that provides methods to interact with the API.
    """

    def __init__(self):
        """Initialize the API client with default values."""
        self.token = None
        self.base_url = " http://127.0.0.1:5000/api/v1/"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}" if self.token else None,
        }
        self.timeout = 5

    def login(self, username: str, password: str):
        """
        Send a login request to the API.
        :param username: Username for user account
        :param password: password for a user account
        :return: user login details
        """

        url: str = f"{self.base_url}auth/sessions/users"

        results = requests.post(
            url=url,
            json={"username": username, "password": password},
            headers=self.headers,
            timeout=self.timeout,
        )

        if results.status_code == 201:
            self.token = results.json().get("access_token")
            self.headers["Authorization"] = f"Bearer {self.token}"
            return results.json()
        else:
            return results.json()

    def retrieve_user_info(self) -> dict[str, dict] | None:
        """
        Send a request to retrieve user information.
        :return: Logged-in user account info
        """

        user_profile_url: str = f"{self.base_url}users/current"

        # This is meant to grab current user information
        # specifically for the user_id, which will be used to
        # fetch user account information.
        user_profile_response = requests.get(
            url=user_profile_url,
            headers=self.headers,
            timeout=self.timeout,
        )

        # Check if the request was successful
        if user_profile_response.status_code == 200:
            user_id = user_profile_response.json().get("user").get("id")
            user_accounts_info = requests.get(
                url=f"{self.base_url}users/{user_id}/accounts",
                headers=self.headers,
                timeout=self.timeout,
            )
            if user_accounts_info.status_code == 200:
                return {
                    "user": user_profile_response.json().get("user"),
                    "accounts": user_accounts_info.json(),
                }

        # if the request was not successful, raise an exception
        raise Exception("Failed to retrieve user information from server")

    def create_user(self, email: str, username: str, password: str) -> dict:
        """
        Send a request to create a new user.
        :param email: Email that we will associate with the user account
        :param username: Username for user account
        :param password: password for a user account
        :return: API response
        """

        url: str = f"{self.base_url}users"

        results = requests.post(
            url=url,
            json={"email": email, "username": username, "password": password},
            headers=self.headers,
            timeout=self.timeout,
        )

        return results.json()

    def retrieve_user_transactions(
        self, limit=30, offset=0, transaction_type=None, account_number=None
    ) -> dict:
        url: str = f"{self.base_url}transactions"

        results = requests.get(
            url=url,
            headers=self.headers,
            timeout=self.timeout,
            json={
                "limit": limit,
                "offset": offset,
                "transaction_type": transaction_type,
                "account_number": account_number,
            },
        )

        return results.json()
