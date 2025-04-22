from typing import List

from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QAbstractItemView, QApplication, QSizePolicy, QTableView


class Transaction:
    def __init__(self, amount, date, account_name, balance, status):
        self.amount = amount
        self.date = date
        self.account_name = account_name
        self.balance = balance
        self.status = status


class TransactionTableModel(QStandardItemModel):
    def __init__(self, transactions: List[Transaction]):
        super().__init__()
        self.transaction = transactions

        self.setHorizontalHeaderLabels(
            ["Account name", "Amount", "Balance", "Date", "Status"]
        )
        for transaction in transactions:
            amountItem = QStandardItem(str(transaction.amount))
            dateItem = QStandardItem(transaction.date)
            accountNameItem = QStandardItem(transaction.account_name)
            balanceItem = QStandardItem(str(transaction.balance))
            statusItem = QStandardItem(transaction.status)

            new_row = [accountNameItem, amountItem, balanceItem, dateItem, statusItem]

            self.appendRow(new_row)


class TransactionTableWidget(QTableView):
    def __init__(self, model):
        super().__init__()
        self.setModel(model)
        self.resizeColumnsToContents()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    example_transaction0 = Transaction(
        100, "3/5/2025", "Yadiel is my son", 400, "COMPLETED"
    )
    example_transaction1 = Transaction(
        100, "3/5/2025", "Yadiel is my son", 400, "COMPLETED"
    )
    example_transaction2 = Transaction(
        100, "3/5/2025", "Yadiel is my son", 400, "COMPLETED"
    )
    model = TransactionTableModel(
        [example_transaction0, example_transaction1, example_transaction2]
    )
    table_widget = TransactionTableWidget(model)
    table_widget.show()
    sys.exit(app.exec())
