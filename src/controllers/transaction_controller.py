from controllers.base_controller import BaseController
from src.models.transaction_model import TransactionModel
from src.views.transaction_view import TransactionView


class TransactionController(BaseController):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.view = TransactionView()
        self.model = TransactionModel()
        self.__connect_signals()

    def __connect_signals(self):
        pass
