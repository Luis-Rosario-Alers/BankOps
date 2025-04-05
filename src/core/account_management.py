"""
Account Management Module.

This module handles all bank account operations including creation,
retrieval, updates, and deletion of accounts.
"""

import functools
import logging
from typing import Any, Callable, NoReturn, TypeVar

logger = logging.getLogger(
    "core"
)  # TODO: change this logger to a more sophisticated logging system.

# Type variable for BankAccount subclasses
T = TypeVar("T", bound="BankAccount")
# Type variable for decorated methods like deposit/withdraw
F = TypeVar("F", bound=Callable[..., float])


class BankAccount:
    """
    Base class for all bank accounts.
    """

    bank_accounts: int = 0
    _name: str
    _balance: float
    _interest_rate: float
    _is_locked: bool

    def __init__(self, name: str, balance: float) -> None:
        self._name = name
        self._balance = balance
        self._interest_rate = 0.0
        self._is_locked = False
        BankAccount.bank_accounts += 1

    @staticmethod
    def log_transaction(func: F) -> F:
        """Decorator to log a transaction."""

        @functools.wraps(func)
        def wrapper(self: T, amount: float, *args: Any, **kwargs: Any) -> float:
            result = func(self, amount, *args, **kwargs)
            logger.info(
                f"{func.__name__} of {amount} in {self.__class__.__name__} "
                f""
                f"for {self._name}. New balance: {self._balance}"
            )
            return result

        return wrapper

    @staticmethod
    def _check_if_locked(func: Callable[..., Any]) -> Callable[..., Any]:
        """Decorator to check if an account is locked before executing a method."""

        @functools.wraps(func)
        def wrapper(self: T, *args: Any, **kwargs: Any) -> Any:
            if self._is_locked:
                raise UserWarning("This account is locked")
            return func(self, *args, **kwargs)

        return wrapper

    @classmethod
    def get_all_bank_accounts(cls) -> int:
        return cls.bank_accounts

    def return_name(self) -> str:
        return self._name

    def check_balance(self) -> float:
        return self._balance

    @log_transaction
    @_check_if_locked
    def deposit(self, amount: float) -> float:
        if amount < 0:
            raise ValueError("Deposit amount cannot be negative")
        self._balance += amount
        return self._balance

    @log_transaction
    @_check_if_locked
    def withdraw(self, amount: float) -> float:
        if amount < 0:
            raise ValueError("Withdraw amount cannot be negative")
        if amount <= self._balance:
            self._balance -= amount
            return self._balance
        else:
            raise ValueError("Not enough funds in account.")


class CheckingAccount(BankAccount):
    _overdraft_limit: float

    def __init__(self, name: str, balance: float) -> None:
        super().__init__(name, balance)
        self._overdraft_limit = 500.0

    def deposit(self, amount: float) -> float:
        return super().deposit(amount)

    def withdraw(self, amount: float) -> float:
        if amount > self._balance + self._overdraft_limit:
            raise ValueError("Overdraft limit exceeded")
        if amount < 0:
            raise ValueError("Withdraw amount cannot be negative")
        self._balance -= amount
        return self._balance


class SavingsAccount(BankAccount):
    _interest_rate: float
    _withdraw_limit: int

    def __init__(self, name: str, balance: float) -> None:
        super().__init__(name, balance)
        self._interest_rate = 0.02
        self._withdraw_limit = 6  # limit to how many times you can withdraw

    def deposit(self, amount: float) -> float:
        if self._withdraw_limit <= 0:
            raise UserWarning(
                "You have hit the withdrawal limit, "
                "you will lose access to your money if you deposit"
            )

        return super().deposit(amount)

    def withdraw(self, amount: float) -> float:
        if self._withdraw_limit <= 0:
            raise ValueError("You have reached your withdrawal limit")

        result = super().withdraw(amount)
        self._withdraw_limit -= 1
        return result

    def add_interest(self) -> float:
        self._balance += self._balance * self._interest_rate
        return self._balance


class CDAccount(BankAccount):
    _term: int
    _interest_rate: float
    _is_matured: bool

    def __init__(self, name: str, balance: float, term: int) -> None:
        super().__init__(name, balance)
        self._term = term
        self._interest_rate = 0.05
        self._is_matured = False

    def deposit(self, amount: float) -> NoReturn:
        raise ValueError("You cannot deposit money to CD account")

    def withdraw(self, amount: float) -> float:
        if not self._is_matured:
            raise ValueError("Cannot withdraw from a CD account before maturity")

        return super().withdraw(amount)


if __name__ == "__main__":
    from main import setup_logging

    setup_logging()
    bank_account = CheckingAccount("Luis's Checking Account", 100.0)
    print(bank_account.return_name())
    print(bank_account.check_balance())
    print(bank_account.deposit(5000.0))
    try:
        print(bank_account.withdraw(4000.0))
    except ValueError as e:
        print(e)
    except UserWarning as e:
        print(e)
