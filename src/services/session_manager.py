import logging
from datetime import datetime, timezone

import keyring

logger = logging.getLogger(__name__)


def store_token(access_token: str, expiration: int, api_client) -> None:
    """Stores the JWT access_token and its expiration time."""
    keyring.set_password("BankOpsBanking", "access_token", access_token)
    keyring.set_password("BankOpsBanking", "expiration", str(expiration))

    api_client.token = access_token

    logger.info("JWT access_token stored successfully.")


def get_token() -> str | None:
    """Retrieves the JWT access_token."""
    return keyring.get_password("BankOpsBanking", "access_token")


def clear_token() -> None:
    """Clears the stored JWT access_token."""
    keyring.delete_password("BankOpsBanking", "access_token")
    keyring.delete_password("BankOpsBanking", "expiration")
    logger.info("JWT access_token cleared.")


def check_expiration() -> bool:
    """Checks if the JWT access_token has expired using datetime."""
    expiration_str = keyring.get_password("BankOpsBanking", "expiration")
    if expiration_str is None:
        return True
    try:
        expiration_dt = datetime.fromisoformat(expiration_str)

        now_dt = datetime.now(timezone.utc)

        return expiration_dt < now_dt
    except ValueError:
        logger.error(f"Invalid expiration format stored: {expiration_str}")
        return True


def refresh_token(api_client):
    """Refreshes the JWT access_token to extend session lifetime."""
    access_token = keyring.get_password("BankOpsBanking", "access_token")

    api_client.refresh_token()

    if access_token is None:
        logger.error("access_token not found.")
        return
