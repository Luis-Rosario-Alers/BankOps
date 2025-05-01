from src.controllers.base_controller import BaseController
from src.controllers.dashboard_controller import DashboardController
from src.controllers.transaction_controller import TransactionController
from src.models.main_window_model import MainWindowModel
from src.views.main_window_view import MainWindowView


# noinspection PyAttributeOutsideInit
class MainWindowController(BaseController):
    def __init__(self):
        super().__init__()
        self.view = MainWindowView(self)
        self.model = MainWindowModel(self)
        self.__connect_signals()
        self.initialize()

    def __connect_signals(self):
        pass

    def initialize(self):
        self.dashboard_controller = DashboardController(self)
        self.transaction_controller = TransactionController(self)

        self.view.contentStackedWidget.addWidget(self.dashboard_controller.view)
        self.view.contentStackedWidget.addWidget(self.transaction_controller.view)

        self.view.contentStackedWidget.setCurrentIndex(0)

    def show(self):
        self.view.show()
        self.dashboard_controller.show()
