import logging.config
import os
import sys
from datetime import datetime

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QApplication, QMessageBox

from src.models.login_model import LoginModel
from src.views.login_view import LoginView
from src.views.main_window import main_window


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

    shutdown_requested = Signal()

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("app")
        self.app = QApplication(sys.argv)
        self.login_view = LoginView(model=None)
        self.login_model = LoginModel(login_view=self.login_view)
        self.main_window = main_window()
        self.__connect_signals()
        self.logger.info("ApplicationManager initialized")

    def __connect_signals(self):
        """Connects signals to slots"""
        self.login_model.login_successful.connect(self.on_login_successful)
        self.shutdown_requested.connect(self.shutdown)

    def start(self):
        """Initialize and start the application"""
        self.logger.info("Starting application")

        # Connecting view and model
        self.login_view.model = self.login_model
        self.login_model.login_view = self.login_view

        # show login screen.
        self.login_view.show()

        self.logger.info("Application started successfully")

        return self.app.exec()

    @Slot(dict)
    def on_login_successful(self, user_data: dict) -> None:
        """Handle successful login"""
        self.logger.info(
            f"User logged in: {user_data.get('user').get('username', 'Unknown')}"
        )

        # Hide the login window
        self.login_view.hide()

        # Show the main application window
        self.show_main_window(user_data)

    @Slot()
    def shutdown(self) -> None:
        """Clean shutdown of the application"""

        # seems redundant, but this is just incase we need to
        # perform some cleanup before quitting

        self.logger.info("Application shutting down")

        # Close windows
        if self.login_view:
            self.login_view.close()

        if self.main_window:
            self.main_window.close()

        self.app.quit()

    def show_main_window(self, user_data: dict):
        """Show the main application window"""
        # Placeholder for the main window logic
        self.logger.info("Main window would be shown here")

        self.main_window.show()


def main() -> int | None:
    logger = setup_logging()

    try:
        # Create and start application
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
