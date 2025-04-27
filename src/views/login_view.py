from PySide6.QtWidgets import QMainWindow, QMessageBox

from src.services.api_client_service import APIClient
from src.services.session_manager import SessionManager
from src.ui.generated.ui_login_window import Ui_login_window


class LoginView(QMainWindow, Ui_login_window):
    def __init__(self, model):
        super().__init__()
        self.setupUi(self)
        self.__connect_signals()
        self.model = model

    def __connect_signals(self):
        self.authenticatePushButton.clicked.connect(self.on_authenticate_button_clicked)

    def on_authenticate_button_clicked(self) -> None:
        """Handles click event for the authenticating button."""

        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()

        self.usernameLineEdit.clear()
        self.passwordLineEdit.clear()

        self.model.process_login(username, password, APIClient(), SessionManager())

    def show_success(self, username) -> None:
        """show a success message to user"""
        QMessageBox.information(
            self, "Success", f"Thank you {username}, you are now logged in."
        )

    def show_failure(self, message) -> None:
        """show a failure message to user"""
        QMessageBox.critical(self, "Failure", message)
