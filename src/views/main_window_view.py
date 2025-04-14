from PySide6.QtWidgets import QHBoxLayout, QMainWindow

from src.ui.generated.main_window_ui import Ui_MainWindow
from src.ui.plugins.widgets.summary_card_widget import SummaryCardWidget


class main_window_view(Ui_MainWindow, QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.addSummaryCards()

    def addSummaryCards(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(
            SummaryCardWidget(
                parent=self, title="That's wild...", is_positive=True, value="200"
            )
        )
        layout.addWidget(
            SummaryCardWidget(
                parent=self, title="That's wild...", is_positive=True, value="200"
            )
        )
        layout.addWidget(
            SummaryCardWidget(
                parent=self, title="That's wild...", is_positive=True, value="200"
            )
        )
        self.widget_8.setLayout(layout)
