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

        url = f"{self.base_url}auth/sessions/users"

        results = requests.post(
            url=url,
            json={"username": username, "password": password},
            headers=self.headers,
            timeout=self.timeout,
        )

        if results.status_code == 201:
            self.token = results.json().get("access_token")
            return results.json()
        else:
            return results.json()

    def create_user(self, email: str, username: str, password: str) -> dict:
        """
        Send a request to create a new user.
        :param email: Email that we will associate with the user account
        :param username: Username for user account
        :param password: password for a user account
        :return: API response
        """

        url = f"{self.base_url}users"

        results = requests.post(
            url=url,
            json={"email": email, "username": username, "password": password},
            headers=self.headers,
            timeout=self.timeout,
        )

        if results.status_code == 201:
            return results.json()
        else:
            return results.json()
