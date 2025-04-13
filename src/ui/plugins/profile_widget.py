from PySide6.QtCore import QRect
from PySide6.QtGui import QColor, QPainter, QPixmap, QRegion
from PySide6.QtWidgets import QMenu, QPushButton

from src.ui.plugins import resources_rc  # noqa


class QProfileButton(QPushButton):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.image = QPixmap(":/default_user.jpg")
        if self.image.isNull():
            print("Error: Could not load default user image from resources")
            self.image = QPixmap(32, 32)
            self.image.fill(QColor(200, 200, 200))
        self.setIcon(self.image)

        self.is_hovered = False
        menu = QMenu(self, title="Profile Menu")
        menu.addAction("Change Profile Picture")
        menu.addAction("Logout")
        self.setMenu(menu)

        self.__connect_signals()

    def __connect_signals(self) -> None:
        self.clicked.connect(self.handle_click)

    @staticmethod
    def handle_click() -> None:
        print("Button clicked!")

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        center_x = self.width() / 2
        center_y = self.height() / 2
        radius = min(center_x, center_y) * 0.8

        Ellipse = QRect(center_x - radius, center_y - radius, 2 * radius, 2 * radius)
        self.setMask(QRegion(Ellipse, QRegion.Ellipse))

        if self.is_hovered:
            color = QColor().fromString("#701E88E5")
            painter.setBrush(color)
            painter.setPen("black")
        else:
            painter.setPen("gray")

        painter.drawPixmap(Ellipse, self.image)
        painter.drawEllipse(Ellipse)

    def enterEvent(self, event) -> None:
        self.is_hovered = True
        self.update()

    def leaveEvent(self, event) -> None:
        self.is_hovered = False
        self.update()
