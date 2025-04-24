from unittest.mock import patch

import pytest

from src.ui.plugins.widgets.account_card_widget import AccountCardWidget
from src.ui.plugins.widgets.summary_card_widget import SummaryCardWidget
from src.ui.plugins.widgets.transaction_table_widget import TransactionTableWidget
from src.views.main_window_view import main_window_view


class TestMainWindowView:
    @patch("src.views.main_window_view.SummaryCardWidget", wraps=SummaryCardWidget)
    def test_add_summary_cards(self, summary_card_widget, qtbot):
        # Arrange
        view = main_window_view()
        qtbot.add_widget(view)

        # Act
        view.addSummaryCards()

        # Assert
        assert view._summary_cards_added is True
        assert summary_card_widget.call_count == 3

    @pytest.mark.parametrize(
        "accounts",
        [
            [
                {
                    "account_name": "Test Account",
                    "balance": 1000,
                    "account_type": "Savings",
                    "account_number": "123456789",
                    "latest_balance_change": "50",
                }
            ],
            [
                {
                    "account_name": "Checking Account",
                    "balance": 2000,
                    "account_type": "Checking",
                    "account_number": "987654321",
                    "latest_balance_change": "100",
                }
            ],
            [
                {
                    "account_name": "Savings Account",
                    "balance": 5000,
                    "account_type": "Savings",
                    "account_number": "456789123",
                    "latest_balance_change": "200",
                }
            ],
        ],
    )
    @patch("src.views.main_window_view.AccountCardWidget", wraps=AccountCardWidget)
    def test_add_account_cards(self, account_card_widget, accounts, qtbot):
        # Arrange
        view = main_window_view()
        qtbot.add_widget(view)
        view.cached_user_info = {"user_accounts": {"accounts": accounts}}

        # Act
        view.addAccountCards()

        # Assert
        assert view._account_cards_added is True
        assert account_card_widget.call_count == len(accounts)
        for _, account in enumerate(accounts):
            account_card_widget.assert_any_call(
                name=account["account_name"],
                balance=account["balance"],
                account_type=account["account_type"],
                account_number=account["account_number"],
                recent_change=account["latest_balance_change"],
            )

    @pytest.mark.parametrize(
        "transactions",
        [
            [
                {
                    "account_from": "123",
                    "account_to": "456",
                    "account_name": "Test Account",
                    "amount": 100,
                    "timestamp": "2023-10-01T12:00:00",
                    "balance_after": 900,
                    "status": "Completed",
                }
            ],
            [
                {
                    "account_from": "789",
                    "account_to": "012",
                    "account_name": "Savings Account",
                    "amount": 500,
                    "timestamp": "2023-10-02T14:30:00",
                    "balance_after": 1500,
                    "status": "Pending",
                },
            ],
            [
                {
                    "account_from": "345",
                    "account_to": "678",
                    "account_name": "Checking Account",
                    "amount": 250,
                    "timestamp": "2023-10-03T09:15:00",
                    "balance_after": 750,
                    "status": "Completed",
                }
            ],
        ],
    )
    @patch(
        "src.views.main_window_view.TransactionTableWidget",
        wraps=TransactionTableWidget,
    )
    @patch("src.views.main_window_view.APIClient")
    def test_add_transaction_table(
        self, mock_api_client_class, mock_transaction_table_widget, transactions, qtbot
    ):
        # Arrange
        mock_api_client_instance = mock_api_client_class.return_value
        mock_api_client_instance.retrieve_user_transactions.return_value = {
            "transactions": transactions
        }
        mock_api_client_instance.get_account_details.return_value = {
            "account_name": "Test Account"
        }
        view = main_window_view()
        view.api_client = mock_api_client_instance
        qtbot.add_widget(view)

        # Act
        view.addTransactionTable()

        # Assert
        assert mock_transaction_table_widget.call_count == 1
        mock_api_client_instance.retrieve_user_transactions.assert_called_once()
        mock_api_client_instance.get_account_details.assert_any_call(
            transactions[0]["account_from"], "account_name"
        )
