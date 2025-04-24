from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QVBoxLayout

from src.services.api_client_service import APIClient
from src.ui.generated.main_window_ui import Ui_MainWindow
from src.ui.plugins.widgets.account_card_widget import AccountCardWidget
from src.ui.plugins.widgets.summary_card_widget import SummaryCardWidget
from src.ui.plugins.widgets.transaction_table_widget import (
    Transaction,
    TransactionTableModel,
    TransactionTableWidget,
)


class main_window_view(Ui_MainWindow, QMainWindow):
    window_shown = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # this is because it needs to match the maximum size of
        # the account card widget so that it can stay consistent UI wise.
        self.widget_9.setMaximumWidth(500)
        # the same thing for this widget as it holds the transaction summary widget.
        self.widget_10.setMaximumWidth(500)
        self._summary_cards_added = False
        self._account_cards_added = False
        self.cached_user_info = None
        self.api_client = APIClient()

    def addSummaryCards(self):
        """
        This method adds the summary cards to the dashboard.
        :return: None
        """
        layout = QHBoxLayout(self.widget_8)
        number_of_cards = 3

        for i in range(number_of_cards):
            layout.addWidget(
                SummaryCardWidget(
                    parent=layout.parent(),
                    title=f"Card {i + 1}",
                    is_positive=True,
                    value="200",
                )
            )
        self._summary_cards_added = True

    def addAccountCards(self):
        """
        This method adds the account cards to the dashboard.
        This method is a work in progress...
        :return: None
        """
        layout = QVBoxLayout(self.widget_15)

        # I know it looks weird, but this is because
        # of the way that the user_info data is set up.
        for account in self.cached_user_info.get("user_accounts").get("accounts"):
            layout.addWidget(
                AccountCardWidget(
                    name=account.get("account_name"),
                    balance=account.get("balance"),
                    account_type=account.get("account_type"),
                    account_number=account.get("account_number"),
                    recent_change=account.get("latest_balance_change"),
                )
            )

        self._account_cards_added = True

    def addTransactionTable(self):
        layout = QHBoxLayout(self.widget_17)
        try:
            transactions = self.api_client.retrieve_user_transactions()

            transactions_list = []

            for transaction in transactions.get("transactions"):
                associated_account_name = self.api_client.get_account_details(
                    transaction.get("account_from"), "account_name"
                ).get("account_name")

                transaction_obj = Transaction(
                    transaction.get("amount"),
                    str(transaction.get("timestamp")),
                    associated_account_name,
                    # TODO: find way to identify account in transaction.
                    transaction.get("balance_after"),
                    transaction.get("status"),
                )
                transactions_list.append(transaction_obj)

            model = TransactionTableModel(transactions_list)

            table_view = TransactionTableWidget(model)
            layout.addWidget(table_view)
        except Exception as e:
            print(e)

    def initialize_dashboard(self):
        pass

    def showEvent(self, event):
        super().showEvent(event)
        if not self._summary_cards_added:
            self.addSummaryCards()
        if not self._account_cards_added:
            self.addAccountCards()
        self.addTransactionTable()
