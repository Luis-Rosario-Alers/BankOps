import logging

import pytest

from src.models.account_model import (
    BankAccountModel,
    CDAccountModel,
    CheckingAccountModel,
    SavingsAccountModel,
)

# Suppress logging during tests unless specifically needed
logging.getLogger("core").setLevel(logging.CRITICAL + 1)

# --- Fixtures ---


@pytest.fixture
def bank_account() -> BankAccountModel:
    """Fixture for a basic BankAccountModel instance."""
    # Reset class variable before each test using this fixture
    initial_count = BankAccountModel.bank_accounts
    account = BankAccountModel("Test User", 100.0)
    yield account
    # Reset count after test to avoid side effects between tests
    BankAccountModel.bank_accounts = initial_count


@pytest.fixture
def checking_account() -> CheckingAccountModel:
    """Fixture for a CheckingAccountModel instance."""
    return CheckingAccountModel("Checking User", 200.0)


@pytest.fixture
def savings_account() -> SavingsAccountModel:
    """Fixture for a SavingsAccountModel instance."""
    return SavingsAccountModel("Savings User", 1000.0)


@pytest.fixture
def cd_account() -> CDAccountModel:
    """Fixture for a CDAccountModel instance."""
    return CDAccountModel("CD User", 5000.0, 12)  # 12-month term


# --- Test BankAccountModel ---


def test_bank_account_initialization(bank_account: BankAccountModel):
    """Test BankAccountModel initialization attributes."""
    assert bank_account.return_name() == "Test User"
    assert bank_account.check_balance() == 100.0
    assert bank_account._interest_rate == 0.0
    assert not bank_account._is_locked


def test_bank_account_count():
    """Test the static counter for bank accounts."""
    initial_count = BankAccountModel.bank_accounts
    acc1 = BankAccountModel("User 1", 10)  # noqa: F841
    assert BankAccountModel.get_all_bank_accounts() == initial_count + 1
    acc2 = BankAccountModel("User 2", 20)  # noqa: F841
    assert BankAccountModel.get_all_bank_accounts() == initial_count + 2
    # Reset manually here as fixture cleanup won't apply retroactively
    BankAccountModel.bank_accounts = initial_count


@pytest.mark.parametrize(
    "amount, expected_balance",
    [
        (50.0, 150.0),
        (0.0, 100.0),
        (0.01, 100.01),
    ],
)
def test_bank_account_deposit_valid(
    bank_account: BankAccountModel, amount: float, expected_balance: float
):
    """Test valid deposits."""
    assert bank_account.deposit(amount) == expected_balance
    assert bank_account.check_balance() == expected_balance


def test_bank_account_deposit_negative(bank_account: BankAccountModel):
    """Test negative deposit raises ValueError."""
    initial_balance = bank_account.check_balance()
    with pytest.raises(ValueError, match="Deposit amount cannot be negative"):
        bank_account.deposit(-50.0)
    assert bank_account.check_balance() == initial_balance  # Balance unchanged


@pytest.mark.parametrize(
    "amount, expected_balance",
    [
        (30.0, 70.0),
        (100.0, 0.0),
        (0.01, 99.99),
    ],
)
def test_bank_account_withdraw_valid(
    bank_account: BankAccountModel, amount: float, expected_balance: float
):
    """Test valid withdrawals."""
    assert bank_account.withdraw(amount) == expected_balance
    assert bank_account.check_balance() == pytest.approx(
        expected_balance
    )  # Use approx for float comparisons


def test_bank_account_withdraw_insufficient_funds(bank_account: BankAccountModel):
    """Test withdrawal with insufficient funds raises ValueError."""
    initial_balance = bank_account.check_balance()
    with pytest.raises(ValueError, match="Not enough funds"):
        bank_account.withdraw(initial_balance + 0.01)
    assert bank_account.check_balance() == initial_balance  # Balance unchanged


def test_bank_account_withdraw_negative(bank_account: BankAccountModel):
    """Test negative withdrawal raises ValueError."""
    initial_balance = bank_account.check_balance()
    with pytest.raises(ValueError, match="Withdraw amount cannot be negative"):
        bank_account.withdraw(-50.0)
    assert bank_account.check_balance() == initial_balance  # Balance unchanged


def test_bank_account_locked_deposit(bank_account: BankAccountModel):
    """Test deposit raises UserWarning on a locked account."""
    bank_account._is_locked = True
    with pytest.raises(UserWarning, match="This account is locked"):
        bank_account.deposit(50.0)


def test_bank_account_locked_withdraw(bank_account: BankAccountModel):
    """Test withdraw raises UserWarning on a locked account."""
    bank_account._is_locked = True
    with pytest.raises(UserWarning, match="This account is locked"):
        bank_account.withdraw(50.0)


# --- Test CheckingAccountModel ---


def test_checking_account_initialization(checking_account: CheckingAccountModel):
    """Test CheckingAccountModel initialization."""
    assert checking_account.check_balance() == 200.0
    assert checking_account._overdraft_limit == 500.0


def test_checking_account_deposit(checking_account: CheckingAccountModel):
    """Test deposit works as inherited."""
    assert checking_account.deposit(50.0) == 250.0
    assert checking_account.check_balance() == 250.0


@pytest.mark.parametrize(
    "withdraw_amount, expected_balance",
    [
        (100.0, 100.0),  # Within balance
        (200.0, 0.0),  # Exactly balance
        (300.0, -100.0),  # Using overdraft
        (700.0, -500.0),  # Max overdraft (balance + limit)
    ],
)
def test_checking_account_withdraw_valid(
    checking_account: CheckingAccountModel,
    withdraw_amount: float,
    expected_balance: float,
):
    """Test valid withdrawals including overdraft."""
    assert checking_account.withdraw(withdraw_amount) == expected_balance
    assert checking_account.check_balance() == expected_balance


def test_checking_account_withdraw_exceeding_overdraft(
    checking_account: CheckingAccountModel,
):
    """Test withdrawing more than balance + overdraft limit."""
    initial_balance = checking_account.check_balance()
    max_withdraw = initial_balance + checking_account._overdraft_limit
    with pytest.raises(ValueError, match="Overdraft limit exceeded"):
        checking_account.withdraw(max_withdraw + 0.01)
    assert checking_account.check_balance() == initial_balance  # Balance unchanged


# --- Test SavingsAccountModel ---


def test_savings_account_initialization(savings_account: SavingsAccountModel):
    """Test SavingsAccountModel initialization."""
    assert savings_account.check_balance() == 1000.0
    assert savings_account._interest_rate == 0.02
    assert savings_account._withdraw_limit == 6


def test_savings_account_add_interest(savings_account: SavingsAccountModel):
    """Test interest calculation."""
    initial_balance = savings_account.check_balance()
    interest = initial_balance * savings_account._interest_rate
    expected_balance = initial_balance + interest
    assert savings_account.add_interest() == expected_balance
    assert savings_account.check_balance() == expected_balance


def test_savings_account_withdraw_within_limit(savings_account: SavingsAccountModel):
    """Test withdrawal decrements limit."""
    initial_limit = savings_account._withdraw_limit
    withdraw_amount = 100.0
    expected_balance = savings_account.check_balance() - withdraw_amount

    assert savings_account.withdraw(withdraw_amount) == expected_balance
    assert savings_account.check_balance() == expected_balance
    assert savings_account._withdraw_limit == initial_limit - 1


def test_savings_account_withdraw_hitting_limit(savings_account: SavingsAccountModel):
    """Test withdrawing until the limit is reached."""
    initial_limit = savings_account._withdraw_limit
    withdraw_amount = 50.0

    # Withdraw exactly 'limit' times
    for i in range(initial_limit):
        savings_account.withdraw(withdraw_amount)
        assert savings_account._withdraw_limit == initial_limit - (i + 1)

    # The Limit should now be 0
    assert savings_account._withdraw_limit == 0

    # The Next withdrawal should fail
    initial_balance = savings_account.check_balance()
    with pytest.raises(ValueError, match="You have reached your withdrawal limit"):
        savings_account.withdraw(withdraw_amount)
    assert savings_account._withdraw_limit == 0  # Limit remains 0
    assert savings_account.check_balance() == initial_balance  # Balance unchanged


def test_savings_account_deposit_when_limit_reached(
    savings_account: SavingsAccountModel,
):
    """Test depositing after withdrawal limit is 0 raises UserWarning."""
    savings_account._withdraw_limit = 0  # Manually set limit to 0
    initial_balance = savings_account.check_balance()
    deposit_amount = 100.0

    with pytest.raises(UserWarning, match="hit the withdrawal limit"):
        savings_account.deposit(deposit_amount)
    # The Balance should remain unchanged because the warning
    # is raised before the deposit occurs
    assert savings_account.check_balance() == initial_balance


def test_savings_account_deposit_when_limit_ok(savings_account: SavingsAccountModel):
    """Test deposit works when limit is not reached."""
    assert savings_account._withdraw_limit > 0
    initial_balance = savings_account.check_balance()
    deposit_amount = 100.0
    expected_balance = initial_balance + deposit_amount
    assert savings_account.deposit(deposit_amount) == expected_balance
    assert savings_account.check_balance() == expected_balance


# --- Test CDAccountModel ---


def test_cd_account_initialization(cd_account: CDAccountModel):
    """Test CDAccountModel initialization."""
    assert cd_account.check_balance() == 5000.0
    assert cd_account._term == 12
    assert cd_account._interest_rate == 0.05
    assert not cd_account._is_matured


def test_cd_account_deposit_fails(cd_account: CDAccountModel):
    """Test depositing into a CD account always fails."""
    initial_balance = cd_account.check_balance()
    with pytest.raises(ValueError, match="cannot deposit money to CD account"):
        cd_account.deposit(1000.0)
    assert cd_account.check_balance() == initial_balance  # Balance unchanged


def test_cd_account_withdraw_before_maturity(cd_account: CDAccountModel):
    """Test withdrawing before maturity fails."""
    assert not cd_account._is_matured  # Ensure it's not matured
    initial_balance = cd_account.check_balance()
    with pytest.raises(
        ValueError, match="Cannot withdraw from a CD account before maturity"
    ):
        cd_account.withdraw(1000.0)
    assert cd_account.check_balance() == initial_balance  # Balance unchanged


def test_cd_account_withdraw_after_maturity(cd_account: CDAccountModel):
    """Test withdrawing after maturity succeeds."""
    cd_account._is_matured = True  # Manually set maturity for testing
    initial_balance = cd_account.check_balance()
    withdraw_amount = 1000.0
    expected_balance = initial_balance - withdraw_amount

    assert cd_account.withdraw(withdraw_amount) == expected_balance
    assert cd_account.check_balance() == expected_balance
