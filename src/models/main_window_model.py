from typing import Any, Dict, Optional

from PySide6.QtCore import QObject, Signal, Slot

from src.services.api_client_service import APIClient, APIClientError
from src.ui.plugins.widgets.transaction_table_widget import Transaction


class MainWindowModel(QObject):
    summary_data_ready = Signal(list)
    account_data_ready = Signal(list)
    transaction_data_ready = Signal(list)
    error_occurred = Signal(str)

    def __init__(self, controller):
        super().__init__()
        self.api_client = APIClient()
        self._cached_user_info: Optional[Dict[str, Any]] = None
        self.controller = controller

    @Slot()
    def fetch_summary_data(self):
        """
        Fetches data for the summary cards.
        TODO: Replace with actual data fetching at some point
        """
        try:
            number_of_cards = 3
            summary_data = []
            for i in range(number_of_cards):
                summary_data.append(
                    {"title": f"Card {i + 1}", "value": "200", "is_positive": True}
                )
            self.summary_data_ready.emit(summary_data)
        except Exception as e:
            self.error_occurred.emit(f"Error fetching summary data: {e}")

    @Slot()
    def fetch_account_data(self):
        """
        Fetches user account information from the API.
        Caches the user info locally.
        """
        try:
            if not self._cached_user_info:
                self._cached_user_info = self.api_client.retrieve_user_info()

            accounts = self._cached_user_info.get("user_accounts", {}).get(
                "accounts", []
            )

            account_list_for_view = [
                {
                    "account_name": acc.get("account_name"),
                    "balance": acc.get("balance"),
                    "account_type": acc.get("account_type"),
                    "account_number": acc.get("account_number"),
                    "latest_balance_change": acc.get("latest_balance_change"),
                }
                for acc in accounts
            ]
            self.account_data_ready.emit(account_list_for_view)

        except APIClientError as e:
            self.error_occurred.emit(f"API Error fetching account data: {e}")
            self._cached_user_info = None
        except Exception as e:
            self.error_occurred.emit(f"Unexpected error fetching account data: {e}")
            self._cached_user_info = None

    @Slot()
    def fetch_transaction_data(self):
        """
        Fetches transaction data from the API and resolves account names.
        """
        try:
            name_cache = {}
            transactions_response = self.api_client.retrieve_user_transactions()
            transactions = transactions_response.get("transactions", [])

            processed_transactions = []
            for transaction in transactions:
                account_number = str(transaction.get("account_from"))
                associated_account_name = "N/A"
                try:
                    if account_number not in name_cache:
                        account_name = self.api_client.get_account_details(
                            account_number, "account_name"
                        ).get("account_name")
                        name_cache[str(account_number)] = account_name
                        associated_account_name = account_name
                    else:
                        associated_account_name = name_cache.get(
                            f"{account_number}", "N/A"
                        )
                except APIClientError as e:
                    print(
                        f"Warning: Could not fetch details for "
                        f"account {account_number}: {e}"
                    )

                transaction_data = {
                    "amount": transaction.get("amount"),
                    "date": str(transaction.get("timestamp")),
                    "account_name": associated_account_name,
                    "balance": transaction.get("balance_after"),
                    "status": transaction.get("status"),
                }

                transaction_obj = Transaction(**transaction_data)
                processed_transactions.append(transaction_obj)

            self.transaction_data_ready.emit(processed_transactions)

        except APIClientError as e:
            self.error_occurred.emit(f"API Error fetching transactions: {e}")
        except Exception as e:
            self.error_occurred.emit(f"Unexpected error fetching transactions: {e}")

    @Slot()
    def initialize_dashboard_data(self):
        """Fetches all necessary data for the dashboard."""
        self.fetch_summary_data()
        self.fetch_account_data()
        self.fetch_transaction_data()
