import sys

from PySide6.QtCore import (
    Property,
    QAbstractAnimation,
    QEasingCurve,
    QEvent,
    QPoint,
    QPropertyAnimation,
    QSequentialAnimationGroup,
    QSize,
    Qt,
)
from PySide6.QtGui import QFont, QPainter, QResizeEvent
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
        self.recent_change = float(recent_change)

        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        self.setMaximumSize(QSize(500, 100))

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

        balance_font = QFont("Roboto Condensed", 12, QFont.Bold, italic=True)
        account_type_font = QFont("Roboto", 8, QFont.Normal)
        account_number_font = QFont("Roboto Condensed", 8, QFont.Light, italic=True)
        account_name_font = QFont("Roboto Condensed", 15, QFont.Normal)
        recent_change_font = QFont("Roboto", 7, QFont.Medium)
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
            "background-color: #BDBDBD; border-radius: 5px; padding: 1px;"
        )
        self.recent_change_label.setFont(recent_change_font)

        self.account_type_label = QLabel(self, text=self.account_type)
        self.account_type_label.setFont(account_type_font)
        self.account_type_label.setStyleSheet("color: #000000;")

        self.account_number_label = QLabel(
            self, text=f"Account number: {str(self.account_number)}"
        )
        self.account_number_label.setFont(account_number_font)
        self.account_number_label.setStyleSheet("color: #F0BDBDBD; ")

        self.rightLayout.addWidget(self.balanceLabel, alignment=Qt.AlignRight)
        self.rightLayout.addWidget(self.recent_change_label, alignment=Qt.AlignRight)
        self.rightLayout.addWidget(self.account_type_label, alignment=Qt.AlignRight)
        self.rightLayout.addWidget(self.account_number_label, alignment=Qt.AlignRight)

        # setup left widget containing account name
        self.account_name_label = QLabel(self, text=self.name)
        self.account_name_label.setStyleSheet("color: #000000;")
        self.account_name_label.setFont(account_name_font)

        self.leftLayout.addWidget(self.account_name_label)

        # add widgets to central layout
        self.centralLayout.addWidget(self.leftWidget)
        self.centralLayout.addWidget(self.rightWidget)

        self.anchor = 0

        self.hover_animation = QPropertyAnimation(self, b"pos", self)
        self.hover_animation.setEasingCurve(QEasingCurve.OutElastic)
        self.hover_animation.setDuration(400)

        self.animations_group = QSequentialAnimationGroup(self)
        self.animations_group.addAnimation(self.hover_animation)

    def start_hover_animation(self):
        """Trigger hover animation based on hover state."""
        self.animations_group.stop()
        if self._is_hovered:
            self.hover_animation.setEndValue(QPoint(self.x() - 10, self.y()))
        else:
            self.hover_animation.setEndValue(self.anchor)

        self.animations_group.start()

    def paintEvent(self, event) -> None:
        """Custom paint event for the card."""
        painter = QPainter(self)

        painter.drawRect(self.contentsRect())
        painter.end()

    def enterEvent(self, event: QEvent):
        """Handle mouse enter event (start hover animation)."""
        self._is_hovered = True
        self.start_hover_animation()

    def leaveEvent(self, event: QEvent):
        """Handle mouse leave event (reverse hover animation)."""
        self._is_hovered = False
        self.start_hover_animation()

    def showEvent(self, event):
        """Set anchor position when widget is shown."""
        super().showEvent(event)
        # this is needed to set the anchor position as soon the widget
        # is shown to the user.

        if not hasattr(self, "_anchor_set") or not self._anchor_set:
            self.anchor = self.pos()
            self._anchor_set = True

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Update anchor and stop animation on resize."""
        super().resizeEvent(event)
        # Stop the animations group BEFORE a resize
        # as this prevents the anchor from accidentally
        # anchoring to different position than the layout
        # calculated one.
        self.animations_group.stop()
        self.set_anchor(self.pos())

    @Property(QPoint)
    def get_anchor(self):
        """Get the anchor position."""
        return self.anchor

    def set_anchor(self, new_position):
        """Set anchor position if not animating."""
        # this is to avoid anchor misplacement because of animations.
        if self.animations_group.state() != QAbstractAnimation.Running:
            self.anchor = new_position
            print(f"Anchor updated to: {new_position}")
            return
        else:
            print(f"{self.animations_group.state()}, ignoring anchor update.")


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
