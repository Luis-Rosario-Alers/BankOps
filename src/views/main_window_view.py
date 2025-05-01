from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMainWindow

from src.ui.generated.ui_main_window import Ui_MainWindow


class MainWindowView(Ui_MainWindow, QMainWindow):
    window_shown = Signal()

    def __init__(self, controller) -> None:
        super().__init__()
        self.setupUi(self)
        self.controller = controller

    def showEvent(self, event):
        super().showEvent(event)
        self.window_shown.emit()
