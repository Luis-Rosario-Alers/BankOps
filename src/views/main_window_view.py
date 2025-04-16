from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QMainWindow

from src.ui.generated.main_window_ui import Ui_MainWindow
from src.ui.plugins.widgets.summary_card_widget import SummaryCardWidget


class main_window_view(Ui_MainWindow, QMainWindow):
    window_shown = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._cards_added = False

    def addSummaryCards(self):
        """
        This method adds the summary cards to the dashboard.
        :return: None
        """
        layout = QHBoxLayout(self.widget_8)
        layout.setContentsMargins(5, 5, 5, 5)
        number_of_cards = 3

        for i in range(number_of_cards):
            layout.addWidget(
                SummaryCardWidget(
                    parent=layout.parent(),
                    title=f"Card {i+1}",
                    is_positive=True,
                    value="200",
                )
            )
        self._cards_added = True

    def showEvent(self, event):
        super().showEvent(event)
        if not self._cards_added:
            self.addSummaryCards()
