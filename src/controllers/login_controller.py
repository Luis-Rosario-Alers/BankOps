from PySide6.QtCore import Signal

from controllers.base_controller import BaseController


class LoginController(BaseController):

    login_successful = Signal()

    def __init__(self, login_view, login_model):
        super().__init__()
        self.login_view = login_view
        self.login_model = login_model
        self.__connect_signals()

    def __connect_signals(self):
        pass

    def process_login(self):

        pass  # TODO: Create server api to process login.
