from app_dir.models.transaction_model import Transaction
from PySide6.QtCore import QObject, Signal, Slot

from src.services.api_client_service import APIClient, APIClientError


class TransactionModel(QObject):
    loading_started = Signal()
    loading_finished = Signal()
    transaction_data_ready = Signal(list)
    error_occurred = Signal(str)

    def __init__(self):
        super().__init__()
        self.transaction_data = []
        self.name_cache = {}
        self.loading_started = Signal()
        self.loading_finished = Signal()
        self.api_client = APIClient()

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
