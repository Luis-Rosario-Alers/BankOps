from PySide6.QtCore import Signal

from controllers.base_controller import BaseController
from services.api_client_service import APIClient


class LoginModel(BaseController):
    login_successful = Signal()

    def __init__(self, login_view):
        super().__init__()
        self.login_view = login_view
        self.__connect_signals()

    def __connect_signals(self):
        pass

    def process_login(self, username: str, password: str):
        api_client = APIClient()

        response = api_client.login(username, password)

        if response.get("access_token"):
            # Emit signal to indicate successful login
            self.login_successful.emit()
            self.login_view.show_success(username)
        else:
            self.login_view.show_failure()
