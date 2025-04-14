from PySide6.QtCore import Signal

from src.controllers.base_controller import BaseController


class LoginModel(BaseController):
    login_successful = Signal(dict)

    def __init__(self, login_view):
        super().__init__()
        self.login_view = login_view
        self.__connect_signals()

    def __connect_signals(self):
        pass

    def process_login(self, username: str, password: str, api_client):
        login_response: dict = api_client.login(username, password)
        try:
            # this ensures we get an auth token back from the server.
            if login_response.get("access_token"):
                user_data = api_client.retrieve_user_info()
                self.login_successful.emit(user_data)
                return user_data
            else:
                # Handle invalid credentials
                error_message = login_response.get("error", "Unknown error occurred.")
                self.login_view.show_failure(error_message)
        except Exception as e:
            # Handle any exceptions that occur during the login process
            self.login_view.show_failure(f"An error occurred: {str(e)}")
