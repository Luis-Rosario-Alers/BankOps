from src.controllers.base_controller import BaseController
from src.models.transaction_model import TransactionModel
from src.views.transaction_view import TransactionView


class TransactionController(BaseController):
    def __init__(self, main_controller):
        super().__init__()
        self.view = TransactionView()
        self.model = TransactionModel()
        self.main_controller = main_controller
        self.__connect_signals()

    def __connect_signals(self):
        pass
