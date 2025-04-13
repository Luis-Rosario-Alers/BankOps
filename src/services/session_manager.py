import logging


class SessionManager:
    """Manages user session, including JWT storage and retrieval."""

    # TODO: implement token expiration check and refresh logic

    # TODO: implement token storage logic. (e.g., in a file or keyring)

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self._jwt_token = None
        self._token_expiration = None

    def store_token(self, token: str, expiration: int) -> None:
        """Stores the JWT token and its expiration time."""
        self._jwt_token = token
        self._token_expiration = expiration
        self.logger.info("JWT token stored successfully.")

    def get_token(self) -> str | None:
        """Retrieves the JWT token."""
        return self._jwt_token

    def clear_token(self) -> None:
        """Clears the stored JWT token."""
        self._jwt_token = None
        self.logger.info("JWT token cleared.")
