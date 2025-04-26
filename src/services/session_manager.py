import logging
from datetime import datetime, timezone

import keyring
import requests

logger = logging.getLogger(__name__)


class SessionManager:
    """Manages JWT methods and processes."""

    def __init__(self):
        self.access_token = self.get_access_token()
        self.refresh_token = self.get_refresh_token()
        self.base_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.timeout = 5
        self.base_url = " http://127.0.0.1:5000/api/v1/"

    def _get_current_auth_header(self) -> dict:
        """Helper to get the current Authorization header"""
        if self.access_token != "None" and self.access_token is not None:  # nosec
            return {"Authorization": f"Bearer {self.access_token}"}
        return {}

    # ============================
    # Keyring/Storage methods
    # ============================

    def store_token(
        self,
        access_token: str,
        access_token_expire_time,
        refresh_token,
        refresh_token_expire_time,
    ) -> None:
        """Stores the JWT access_token and refresh_token.
        :param refresh_token:
        :param access_token:
        :param access_token_expire_time:
        :param refresh_token_expire_time:
        """
        keyring.set_password("BankOpsBanking", "access_token", access_token)
        keyring.set_password(
            "BankOpsBanking", "access_token_expire_time", access_token_expire_time
        )
        keyring.set_password("BankOpsBanking", "refresh_token", refresh_token)
        keyring.set_password(
            "BankOpsBanking", "refresh_token_expire_time", refresh_token_expire_time
        )

        self.access_token = access_token
        self.refresh_token = refresh_token

        logger.info("JWT access_token and refresh_token stored successfully.")

    def get_access_token(self) -> str | None:
        """Retrieves the JWT access_token."""
        self.access_token = keyring.get_password("BankOpsBanking", "access_token")
        return self.access_token

    def get_refresh_token(self):
        self.refresh_token = keyring.get_password("BankOpsBanking", "refresh_token")
        return self.refresh_token

    def clear_tokens(self) -> None:
        """Clears the stored JWT access_token."""
        keyring.delete_password("BankOpsBanking", "access_token")
        keyring.delete_password("BankOpsBanking", "refresh_token")
        keyring.delete_password("BankOpsBanking", "access_token_expire_time")
        keyring.delete_password("BankOpsBanking", "refresh_token_expire_time")
        # TODO: find a way to not accidentally clear other
        #  tokens that are not necessary.

        self.access_token = None
        self.refresh_token = None

        logger.info("JWT access_token cleared.")

    def check_expiration(self) -> bool:
        """Checks if the JWT access_token has expired using datetime."""
        expiration_str = keyring.get_password(
            "BankOpsBanking", "access_token_expire_time"
        )
        if expiration_str is None:
            return True
        try:
            expiration_dt = datetime.fromtimestamp(int(expiration_str), tz=timezone.utc)

            now_dt = datetime.now(timezone.utc)

            is_expired = now_dt >= expiration_dt
            return is_expired
        except ValueError:
            logger.error(f"Invalid expiration format stored: {expiration_str}")
            self.clear_tokens()
            return True

    # ============================
    # Request-related methods
    # ============================

    def attempt_session_refresh(self, refresh_token: str):
        """Attempts to renew the access token."""
        if not refresh_token:
            raise ValueError("No refresh token available to attempt session renewal.")

        url = f"{self.base_url}auth/sessions/renew"
        # Uses the refresh token specifically for this request's Authorization header
        refresh_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {refresh_token}",
        }

        try:
            results = requests.post(
                url=url,
                headers=refresh_headers,
                timeout=self.timeout,
            )
            results.raise_for_status()

            if results.status_code in [200, 201]:
                response_data = results.json()
                new_access_token = response_data.get("access_token")
                new_access_token_expiration = str(
                    response_data.get("access_token_expires_in")
                )
                new_refresh_token = response_data.get("refresh_token", refresh_token)
                new_refresh_token_expiration = str(
                    response_data.get("refresh_token_expires_in")
                )

                if not new_access_token:
                    raise ValueError(
                        "Refresh response did not contain an access token."
                    )

                self.store_token(
                    new_access_token,
                    new_access_token_expiration,
                    new_refresh_token,
                    new_refresh_token_expiration,
                )

                logger.info("Access token successfully refreshed.")
                return True
            else:
                raise Exception(
                    f"Failed to renew JWT access_token. Status: {results.status_code}"
                )

        except requests.exceptions.RequestException as e:
            logger.error(f"Network or request error during token refresh: {e}")
            raise Exception(
                "Failed to communicate with authentication server for refresh."
            ) from e
        except Exception as e:
            logger.error(f"Error processing token refresh response: {e}")
            # Clears invalid tokens if error occurs during token refresh.
            self.clear_tokens()
            raise

    def ensure_session_valid(self):
        """Checks if the session is valid and attempts refresh if expired."""
        if self.check_expiration():
            logger.info("Access token expired or invalid, attempting refresh.")
            try:
                self.attempt_session_refresh(self.refresh_token)
                return True
            except Exception as e:
                logger.error(f"Session refresh failed: {e}")
                raise ConnectionAbortedError(
                    "Session refresh failed. Please log in again."
                ) from e
        else:
            logger.debug("Session token is currently valid.")
            return True

    def get_authenticated_headers(self) -> dict:
        """
        Ensures the session is valid (refreshes if needed) and returns
        the full headers dictionary required for an authenticated API call.

        :raises: Exception (e.g., ConnectionAbortedError) if refresh fails.
        :return: Dictionary of headers including the valid Authorization header.
        """
        self.ensure_session_valid()  # Check expiry and refresh if needed
        auth_header = self._get_current_auth_header()
        if not auth_header:
            logger.error("Failed to get auth header even after session check.")
            self.clear_tokens()
            raise ConnectionAbortedError(
                "Authentication failed. No valid token available."
            )

        return {**self.base_headers, **auth_header}

    def login(self, username: str, password: str):
        """
        Send a login request to the API.
        :param username: Username of the user account
        :param password: Password of the user account
        :return: user login details
        """

        url: str = f"{self.base_url}auth/sessions/users"
        payload = {"username": username, "password": password}

        results = requests.post(
            url=url,
            json=payload,
            headers=self.base_headers,
            timeout=self.timeout,
        )

        if results.status_code == 201:
            self.store_token(
                access_token=results.json().get("access_token"),
                access_token_expire_time=str(
                    results.json().get("access_token_expires_in")
                ),
                refresh_token=results.json().get("refresh_token"),
                refresh_token_expire_time=str(
                    results.json().get("refresh_token_expires_in")
                ),
            )
            return results.json()
        else:
            return results.json()

    def logout(self):
        """Logout out current user session."""
        logger.info("Logging out user.")
        url: str = f"{self.base_url}auth/sessions/users"
        current_headers = self.get_authenticated_headers()
        results = requests.delete(
            url=url,
            headers=current_headers,
            timeout=self.timeout,
        )
        if results.status_code == 204:
            logger.info("User logged out successfully. Clearing local tokens.")
            self.clear_tokens()
            return
        else:
            raise Exception("Failed to logout user.")
