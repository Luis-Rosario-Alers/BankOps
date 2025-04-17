import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class AccountCardWidget(QFrame):
    def __init__(
        self, name, balance, account_type, account_number, recent_change, parent=None
    ):
        super().__init__()
        self.name = name
        self.balance = balance
        self.account_type = account_type
        self.account_number = account_number
        self.recent_change = recent_change

        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        self.centralLayout = QHBoxLayout()
        self.setLayout(self.centralLayout)

        self.setObjectName("accountCard")

        self.setStyleSheet(
            "background-color: rgb(255, 255, 255);"
            "border-radius: 5px;"
            "font-family: Roboto;"
        )

        font = QFont("Roboto", 20)
        font.setStyleStrategy(QFont.PreferAntialias)

        balance_font = QFont("Roboto Condensed", 20, QFont.Bold, italic=True)
        account_type_font = QFont("Roboto", 14, QFont.Normal)
        account_number_font = QFont("Roboto Condensed", 12, QFont.Light, italic=True)
        account_name_font = QFont("Roboto Condensed", 24, QFont.Normal)
        recent_change_font = QFont("Roboto", 10, QFont.Medium)
        recent_change_font.setItalic(True)

        self.setFont(font)

        self.rightWidget = QWidget()
        self.leftWidget = QWidget()

        self.rightLayout = QVBoxLayout()
        self.rightLayout.setAlignment(Qt.AlignRight)
        self.leftLayout = QVBoxLayout()
        self.leftLayout.setAlignment(Qt.AlignLeft)

        self.rightWidget.setLayout(self.rightLayout)
        self.leftWidget.setLayout(self.leftLayout)

        # setup right widget containing account information
        self.balanceLabel = QLabel(self, text=f"${str(self.balance)}")
        self.balanceLabel.setFont(balance_font)
        self.balanceLabel.setStyleSheet("color: #000000;")

        self.recent_change_frame = QFrame(self)
        self.recent_change_frame.setLayout(QHBoxLayout())

        # check if its positive, negative, or 0
        if self.recent_change > 0:
            self.recent_change_text = f"+{str(self.recent_change)}"
            self.recent_change_text_color = "#43A047"
        elif self.recent_change < 0:
            self.recent_change_text = f"-{str(self.recent_change)}"
            self.recent_change_text_color = "#E53935"
        else:
            self.recent_change_value_status = None
            self.recent_change_text = "0"
            self.recent_change_text_color = "#000000"

        self.recent_change_label = QLabel(self, text=self.recent_change_text)
        self.recent_change_label.setStyleSheet(
            f"color: {self.recent_change_text_color};"
        )
        self.recent_change_label.setFont(recent_change_font)

        self.recent_change_frame.layout().addWidget(self.recent_change_label)
        self.recent_change_frame.setStyleSheet(
            "background-color: #BDBDBD; border-radius: 5px;"
        )

        self.account_type_label = QLabel(self, text=self.account_type)
        self.account_type_label.setFont(account_type_font)
        self.account_type_label.setStyleSheet("color: #000000;")

        self.account_number_label = QLabel(
            self, text=f"Account number: {str(self.account_number)}"
        )
        self.account_number_label.setFont(account_number_font)
        self.account_number_label.setStyleSheet("color: #F0BDBDBD; ")

        self.rightLayout.addWidget(self.balanceLabel)
        self.rightLayout.addWidget(self.recent_change_frame)
        self.rightLayout.addWidget(self.account_type_label)
        self.rightLayout.addWidget(self.account_number_label)

        # setup left widget containing account name
        self.account_name_label = QLabel(self, text=self.name)
        self.account_name_label.setStyleSheet("color: #000000;")
        self.account_name_label.setFont(account_name_font)

        self.leftLayout.addWidget(self.account_name_label)

        # add widgets to central layout
        self.centralLayout.addWidget(self.leftWidget)
        self.centralLayout.addWidget(self.rightWidget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    account_card = AccountCardWidget(
        name="steve account",
        balance=100000,
        account_type="Checking",
        account_number=1234567890,
        recent_change=100,
    )
    account_card.show()
    app.exec()
