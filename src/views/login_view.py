from PySide6.QtWidgets import QMainWindow, QMessageBox

from ui.generated.ui_login_window import Ui_login_window


class LoginView(QMainWindow, Ui_login_window):
    def __init__(self, controller):
        super().__init__()
        self.setupUi(self)
        self.controller = controller

    def on_authenticate_button_clicked(self):
        self.accountNumberLineEdit.clear()
        self.pinLineEdit.clear()
        account_number = int(self.accountNumberLineEdit.text())
        pin = int(self.pinLineEdit.text())
        self.controller.process_login(account_number, pin)

    def show_success(self, username):
        """show a success message to user"""
        QMessageBox.information(
            self, "Success", f"Thank you {username}, you are now logged in."
        )

    def show_failure(self):
        """show a failure message to user"""
        QMessageBox.critical(self, "Failure", "Incorrect account number or pin")
