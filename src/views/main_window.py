from PySide6.QtWidgets import QMainWindow

from src.ui.generated.main_window_ui import Ui_MainWindow


class main_window(Ui_MainWindow, QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # TODO: add functionality to main_window.
