import PySide6.QtCore
from PySide6.QtCore import (
    QEasingCurve,
    QEvent,
    QPoint,
    QPropertyAnimation,
    QSequentialAnimationGroup,
)
from PySide6.QtGui import QFont, QPainter
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout


class SummaryCardWidget(QFrame):
    def __init__(self, title, value, is_positive=True, parent=None):
        self._is_hovered = False
        super().__init__(parent)

        self._raised_position = QPoint(0, 0)
        self.move_animation = QPropertyAnimation(self, b"raised_position", self)
        self.move_animation.setEasingCurve(QEasingCurve.OutElastic)
        self.move_animation.setDuration(400)

        # I haven't created the property for this animation yet.
        # self.animation2 = QPropertyAnimation(self, b"lowered_position", self)
        # self.animation2.setEasingCurve(QEasingCurve.InBounce)
        # self.animation2.setDuration(100)
        # self.animation2.setEndValue(1000)

        self.animations_group = QSequentialAnimationGroup(self)
        self.animations_group.addAnimation(self.move_animation)
        # self.animations_group.addAnimation(self.animation2)

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

    def start_animation(self):
        self.animations_group.stop()
        # FIXME: figure out why this bugs out on window resizes.
        if self._is_hovered:
            self.move_animation.setEndValue(QPoint(self.x(), -10))
        else:
            self.move_animation.setEndValue(QPoint(self.x(), 0))
        self.update()
        self.animations_group.start()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        print("yadiel")
        print(self._raised_position)

        painter.setPen("blue")
        painter.drawRect(self.contentsRect())
        painter.end()

    def enterEvent(self, event: QEvent):
        self._is_hovered = True
        self.start_animation()

    def leaveEvent(self, event: QEvent):
        self._is_hovered = False
        self.start_animation()

    @PySide6.QtCore.Property(QPoint)
    def raised_position(self):
        return self._raised_position

    @raised_position.setter
    def raised_position(self, pos: QPoint):
        if pos != self._raised_position:
            self._raised_position = pos
            self.move(pos)
            self.update()
