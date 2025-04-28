from src.controllers.base_controller import BaseController
from src.models.main_window_model import MainWindowModel
from src.views.main_window_view import MainWindowView


class MainWindowController(BaseController):
    def __init__(self):
        super().__init__()
        self.view = MainWindowView(self)
        self.model = MainWindowModel(self)
        self.__connect_signals()

    def __connect_signals(self):
        # model -> view connections
        self.model.summary_data_ready.connect(self.view.addSummaryCards)
        self.model.account_data_ready.connect(self.view.addAccountCards)
        self.model.transaction_data_ready.connect(self.view.addTransactionTable)

        # view -> model connections
        self.view.window_shown.connect(self.model.initialize_dashboard_data)

    def show(self):
        self.view.show()
