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
        self._summary_cards_added = False
        self._account_cards_added = False

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
                    title=f"Card {i+1}",
                    is_positive=True,
                    value="200",
                )
            )
        self._summary_cards_added = True

    def addAccountCards(self, number_of_accounts):
        """
        This method adds the account cards to the dashboard.
        This method is a work in progress...
        :return: None
        """
        layout = QVBoxLayout(self.widget_15)

        for _ in range(number_of_accounts):
            layout.addWidget(
                AccountCardWidget(
                    name="Steve Checking",
                    balance=100,
                    account_type="Checking",
                    account_number=1234567890,
                    recent_change=200,
                )
            )

        self._account_cards_added = True

    def addTransactionTable(self):
        layout = QHBoxLayout(self.widget_17)
        try:
            api_client = APIClient()

            transactions = api_client.retrieve_user_transactions()

            transactions_list = []

            for transaction in transactions.get("transactions"):
                transaction_obj = Transaction(
                    transaction.get("amount"),
                    str(transaction.get("timestamp")),
                    "placeholder",
                    transaction.get("balance_after"),
                    transaction.get("status"),
                )
                transactions_list.append(transaction_obj)

            model = TransactionTableModel(transactions_list)

            table_view = TransactionTableWidget(model)
            layout.addWidget(table_view)
        except Exception as e:
            print(e)

    def showEvent(self, event):
        super().showEvent(event)
        if not self._summary_cards_added:
            self.addSummaryCards()
        if not self._account_cards_added:
            self.addAccountCards(3)
        self.addTransactionTable()
