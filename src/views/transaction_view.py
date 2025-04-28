from PySide6.QtWidgets import QWidget

from src.ui.generated.ui_Transactions import Ui_transactions


class TransactionView(QWidget, Ui_transactions):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
