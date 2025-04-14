from PySide6.QtGui import QFont
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout


class SummaryCardWidget(QFrame):
    def __init__(self, title, value, is_positive=True, parent=None):
        super().__init__(parent)
        self.setObjectName("summaryCard")

        # Set frame styling
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setStyleSheet(
            """
            #summaryCard {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
        """
        )

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(5)

        # Title label
        self.title_label = QLabel(title)
        self.title_label.setObjectName("cardTitle")
        self.title_label.setStyleSheet("color: #333744; font-size: 14px;")

        value_layout = QHBoxLayout()

        # Value label
        self.value_label = QLabel(value)
        self.value_label.setObjectName("cardValue")
        self.value_label.setFont(QFont("Roboto", 14))
        color = "#1E74EB" if is_positive else "#992E2E"
        self.value_label.setStyleSheet(
            f"color: {color}; font-size: 20px; font-weight: bold;"
        )

        value_layout.addWidget(self.value_label)
        value_layout.addStretch()

        main_layout.addWidget(self.title_label)
        main_layout.addLayout(value_layout)
        main_layout.addStretch()
