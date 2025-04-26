import logging.config
import os
import sys
from datetime import datetime

from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QApplication, QMessageBox

from services.api_client_service import APIClient
from services.session_manager import SessionManager
from src.models.login_model import LoginModel
from src.views.login_view import LoginView
from src.views.main_window_view import main_window_view


def setup_logging():
    log_dir: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    os.makedirs(name=log_dir, exist_ok=True)

    timestamp: str = datetime.now().strftime(format="%Y%m%d_%H%M%S")
    log_file: str = os.path.join(log_dir, f"bankops_{timestamp}.log")

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stderr),
            logging.FileHandler(log_file),
        ],
    )

    logger = logging.getLogger("main")
    logger.info("Application starting up...")
    return logger


class ApplicationManager(QObject):
    """Manages the life cycle of the application"""

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("app")
        self.app = QApplication(sys.argv)

        self.session_manager = SessionManager()
        self.api_client = APIClient()

        self.login_view = LoginView(model=None)
        self.login_model = LoginModel(login_view=self.login_view)
        self.main_window = main_window_view()

        self.__connect_signals()

        self.logger.info("ApplicationManager initialized")

    def __connect_signals(self):
        """Connects signals to slots"""
        self.login_model.login_successful.connect(self.on_login_successful)

    def start(self):
        """Initialize and start the application"""
        self.logger.info("Starting application")

        # Connecting view and model
        self.login_view.model = self.login_model
        self.login_model.login_view = self.login_view

        self.logger.info("Application started successfully")

        self.login_view.show()

        try:
            if self.session_manager.ensure_session_valid():
                user_data = self.api_client.retrieve_user_info()
                self.on_login_successful(user_data=user_data)
                self.login_view.hide()
        except Exception:
            self.logger.error("Failed to re-login user.")

        return self.app.exec()

    @Slot(dict)
    def on_login_successful(self, user_data: dict) -> None:
        """Handle successful login"""
        self.logger.info(
            f"User logged in: "
            f"{user_data.get('user_profile').get('username', 'Unknown')}"
        )

        self.login_view.hide()
        self.main_window.cached_user_info = user_data
        self.main_window.show()


def main() -> int | None:
    logger = setup_logging()

    try:
        # Create and start the application
        app_manager = ApplicationManager()
        app_manager.start()

    except Exception as e:
        logger.exception(f"Unhandled exception: {e}")
        QMessageBox.critical(
            None, "Critical Error", f"A critical error occurred: {str(e)}"
        )
        return 1


if __name__ == "__main__":
    main()
