import logging.config
import os
import sys
from datetime import datetime

from app.services.connection import db_manager
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QApplication, QMessageBox

from controllers.login_controller import LoginController
from models.login_model import LoginModel
from views.login_view import LoginView


def setup_logging():
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"bankops_{timestamp}.log")

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
        self.main_window = None
        self.login_view = None
        self.login_controller = None

        self.shutdown_requested.connect(self.shutdown)

    def start(self):
        """Initialize and start the application"""
        self.logger.info("Starting application")

        connection_string = (
            "mysql+mysqlconnector://root:" "root@localhost/bankops_banking"
        )  # TODO: replace with actual connection string

        if not db_manager.initialize(connection_string):
            self.show_error(
                "Database Connection Error",
                "Could not connect to the database. "
                "Please check your connection settings.",
            )
            return 1

        self.setup_login_screen()

        return self.app.exec()

    def setup_login_screen(self):
        """Set up the login screen"""
        # Create MVC components
        self.login_view = LoginView(None)
        login_model = LoginModel(None)  # The Controller will be set later
        self.login_controller = LoginController(self.login_view, login_model)

        # Set controller reference in a model
        login_model.controller = self.login_controller
        self.login_view.controller = self.login_controller

        # Connect signals
        self.login_controller.login_successful.connect(self.on_login_successful)

        self.login_view.show()

    @Slot(dict)
    def on_login_successful(self, user_data):
        """Handle successful login"""
        self.logger.info(f"User logged in: {user_data.get('name', 'Unknown')}")

        # Hide login window
        self.login_view.hide()

        # TODO: Show main application window
        # self.show_main_window(user_data)

        # For now, just show a message box
        QMessageBox.information(
            None,
            "Login Successful",
            f"Welcome {user_data.get('name', 'User')}!\n"
            f"Main application window would open here.",
        )

    def show_error(self, title, message):
        """Show error dialog"""
        QMessageBox.critical(None, title, message)

    @Slot()
    def shutdown(self):
        """Clean shutdown of the application"""
        self.logger.info("Application shutting down")

        # Close database connections
        db_manager.close()

        # Close windows
        if self.login_view:
            self.login_view.close()

        if self.main_window:
            self.main_window.close()

        self.app.quit()


def main():
    logger = setup_logging()

    try:
        # Create and start application
        app_manager = ApplicationManager()
        return app_manager.start()

    except Exception as e:
        logger.exception(f"Unhandled exception: {e}")
        QMessageBox.critical(
            None, "Critical Error", f"A critical error occurred: {str(e)}"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
