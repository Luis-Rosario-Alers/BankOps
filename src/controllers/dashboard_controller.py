from src.controllers.base_controller import BaseController
from src.models.dashboard_model import DashboardModel
from src.views.dashboard_view import DashboardView


class DashboardController(BaseController):
    def __init__(self, main_controller):
        super().__init__()
        self.main_controller = main_controller
        self.view = DashboardView(self)
        self.model = DashboardModel(self)
        self.__connect_signals()

    def __connect_signals(self):
        # model -> view connections
        self.model.summary_data_ready.connect(self.view.addSummaryCards)
        self.model.account_data_ready.connect(self.view.addAccountCards)
        self.model.transaction_data_ready.connect(self.view.addTransactionTable)

        # view -> model connections
        self.view.widget_shown.connect(self.model.initialize_dashboard_data)

    def show(self):
        self.view.show()
