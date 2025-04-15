from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import QHBoxLayout, QMainWindow

from src.ui.generated.main_window_ui import Ui_MainWindow
from src.ui.plugins.widgets.summary_card_widget import SummaryCardWidget


class main_window_view(Ui_MainWindow, QMainWindow):
    window_shown = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def addSummaryCards(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        number_of_cards = 3

        for _ in range(number_of_cards):
            card = SummaryCardWidget("Hola", "200")
            layout.addWidget(card)
        self.widget_8.setLayout(layout)

    def showEvent(self, event):
        super().showEvent(event)
        self.addSummaryCards()
        QTimer.singleShot(0, self.updateCardPositions)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # this is meant to keep the summary card widgets from
        # keeping the old anchor positions and causing undefined behavior
        QTimer.singleShot(0, self.updateCardPositions)

    def updateCardPositions(self):
        for card in self.findChildren(SummaryCardWidget):
            card.anchor = card.pos()
