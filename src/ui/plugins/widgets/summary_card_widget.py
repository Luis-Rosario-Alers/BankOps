from PySide6.QtCore import (
    Property,
    QAbstractAnimation,
    QEasingCurve,
    QEvent,
    QPoint,
    QPropertyAnimation,
    QSequentialAnimationGroup,
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


class SummaryCardWidget(QFrame):
    """Card widget for displaying a summary value with animation."""

    def __init__(self, title, value, is_positive=True, parent=None):
        """Initialize the summary card with title, value, and color."""
        self._is_hovered = False
        super().__init__(parent)

        self.anchor = 0

        self.hover_animation = QPropertyAnimation(self, b"pos", self)
        self.hover_animation.setEasingCurve(QEasingCurve.OutElastic)
        self.hover_animation.setDuration(400)

        self.animations_group = QSequentialAnimationGroup(self)
        self.animations_group.addAnimation(self.hover_animation)

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

    def start_hover_animation(self):
        """Trigger hover animation based on hover state."""
        self.animations_group.stop()
        if self._is_hovered:
            self.hover_animation.setEndValue(QPoint(self.x(), self.y() - 10))
        else:
            self.hover_animation.setEndValue(self.anchor)

        self.animations_group.start()

    def paintEvent(self, event) -> None:
        """Custom paint event for the card."""
        painter = QPainter(self)

        # TODO: Make the paint event less boring
        painter.setPen("blue")
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
        """Set the anchor position when the widget is shown."""
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
        # anchoring to a different position than the layout-calculated one.
        self.animations_group.stop()
        self.set_anchor(self.pos())

    @Property(QPoint)
    def get_anchor(self):
        """Get the anchor position."""
        return self.anchor

    def set_anchor(self, new_position):
        """Set the anchor position if not animating."""
        # this is to avoid anchor misplacement because of animations.
        if self.animations_group.state() != QAbstractAnimation.Running:
            self.anchor = new_position
            # print(f"Anchor updated to: {new_position}")
            return
        else:
            pass
            # print(f"{self.animations_group.state()}, ignoring anchor update.")


if __name__ == "__main__":
    """Run a demo of the SummaryCardWidget."""
    import sys

    app = QApplication(sys.argv)
    summary_card_widget = SummaryCardWidget("no", "200")
    widget = QWidget()
    widget.setLayout(QHBoxLayout())
    widget.layout().addWidget(summary_card_widget)
    widget.show()
    app.exec()
