from PySide6.QtCore import Signal
from PySide6.QtWidgets import QVBoxLayout, QWidget

from src.ui.generated.ui_dashboard import Ui_Dashboard
from src.ui.plugins.widgets.account_card_widget import AccountCardWidget
from src.ui.plugins.widgets.summary_card_widget import SummaryCardWidget
from src.ui.plugins.widgets.transaction_table_widget import (
    Transaction,
    TransactionTableModel,
    TransactionTableWidget,
)


class DashboardView(QWidget, Ui_Dashboard):
    widget_shown = Signal()

    def __init__(self, controller) -> None:
        super().__init__()
        self.setupUi(self)
        self._summary_cards_added = False
        self._account_cards_added = False
        self.controller = controller

    def addSummaryCards(self, summary_data: list[dict] = None):
        """
        This method adds the summary cards to the dashboard.
        :return: None
        """
        layout = self.widget_8.layout()

        for summary in summary_data:
            layout.addWidget(
                SummaryCardWidget(
                    parent=layout.parent(),
                    title=summary.get("title"),
                    is_positive=summary.get("is_positive"),
                    value=summary.get("value"),
                )
            )

        self._summary_cards_added = True

    def addAccountCards(self, accounts: list[dict] = None):
        """
        This method adds the account cards to the dashboard.
        This method is a work in progress...
        :return: None
        """

        layout = QVBoxLayout(self.widget_15)

        for account in accounts:
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

    def addTransactionTable(self, transactions: list[Transaction] = None):
        layout = self.widget_17.layout()
        try:
            # TODO: Eventually have API provide account_name transaction info instead.

            model = TransactionTableModel(transactions)

            table_view = TransactionTableWidget(model)
            layout.addWidget(table_view)
        except Exception as e:
            print(e)

    def showEvent(self, event):
        super().showEvent(event)
        if not self._account_cards_added or not self._summary_cards_added:
            self.widget_shown.emit()
