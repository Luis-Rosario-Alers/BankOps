from PySide6.QtCore import (
    QCoreApplication,
    QMetaObject,
    QRect,
    QSize,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QIcon,
    QPalette,
    QPixmap,
)
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMenuBar,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from src.ui.plugins.widgets.profile_widget import QProfileButton


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(646, 513)
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush
        )
        brush1 = QBrush(QColor(217, 217, 217, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush1)
        brush2 = QBrush(QColor(120, 120, 120, 255))
        brush2.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Light, brush2)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Dark, brush)
        brush3 = QBrush(QColor(170, 0, 0, 255))
        brush3.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush3)
        palette.setBrush(
            QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush
        )
        brush4 = QBrush(QColor(245, 245, 245, 255))
        brush4.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush4)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush4)
        brush5 = QBrush(QColor(30, 136, 229, 255))
        brush5.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QPalette.ColorGroup.Active, QPalette.ColorRole.Highlight, brush5
        )
        brush6 = QBrush(QColor(25, 118, 210, 255))
        brush6.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Link, brush6)
        palette.setBrush(
            QPalette.ColorGroup.Active, QPalette.ColorRole.LinkVisited, brush5
        )
        brush7 = QBrush(QColor(245, 245, 245, 15))
        brush7.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QPalette.ColorGroup.Active, QPalette.ColorRole.AlternateBase, brush7
        )
        brush8 = QBrush(QColor(255, 193, 7, 255))
        brush8.setStyle(Qt.BrushStyle.SolidPattern)
        # if QT_VERSION >= QT_VERSION_CHECK(6, 6, 0)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Accent, brush8)
        # endif
        palette.setBrush(
            QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush
        )
        palette.setBrush(
            QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush1
        )
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Dark, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush3)
        palette.setBrush(
            QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush
        )
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush4)
        palette.setBrush(
            QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush4
        )
        palette.setBrush(
            QPalette.ColorGroup.Inactive, QPalette.ColorRole.Highlight, brush5
        )
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Link, brush6)
        palette.setBrush(
            QPalette.ColorGroup.Inactive, QPalette.ColorRole.LinkVisited, brush5
        )
        palette.setBrush(
            QPalette.ColorGroup.Inactive, QPalette.ColorRole.AlternateBase, brush7
        )
        # if QT_VERSION >= QT_VERSION_CHECK(6, 6, 0)
        palette.setBrush(
            QPalette.ColorGroup.Inactive, QPalette.ColorRole.Accent, brush8
        )
        # endif
        palette.setBrush(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush
        )
        palette.setBrush(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush1
        )
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Dark, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush)
        palette.setBrush(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush
        )
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush4)
        palette.setBrush(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush4
        )
        brush9 = QBrush(QColor(19, 85, 144, 255))
        brush9.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.Highlight, brush9
        )
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Link, brush6)
        palette.setBrush(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.LinkVisited, brush5
        )
        palette.setBrush(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.AlternateBase, brush7
        )
        # if QT_VERSION >= QT_VERSION_CHECK(6, 6, 0)
        palette.setBrush(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.Accent, brush8
        )
        # endif
        MainWindow.setPalette(palette)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.horizontalLayout_3 = QHBoxLayout(self.widget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_7 = QLabel(self.widget)
        self.label_7.setObjectName("label_7")
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMaximumSize(QSize(40, 40))
        self.label_7.setPixmap(QPixmap(":/dashboard/icons/bank_PNG3-2926375216.png"))
        self.label_7.setScaledContents(True)
        self.label_7.setAlignment(
            Qt.AlignmentFlag.AlignLeading
            | Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.horizontalLayout_3.addWidget(self.label_7, 0, Qt.AlignmentFlag.AlignLeft)

        self.label = QLabel(self.widget)
        self.label.setObjectName("label")
        font = QFont()
        font.setFamilies(["Roboto"])
        font.setPointSize(22)
        font.setBold(False)
        self.label.setFont(font)

        self.horizontalLayout_3.addWidget(self.label, 0, Qt.AlignmentFlag.AlignLeft)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setFamilies(["Roboto"])
        font1.setPointSize(10)
        font1.setItalic(True)
        self.label_5.setFont(font1)
        self.label_5.setAlignment(
            Qt.AlignmentFlag.AlignBottom
            | Qt.AlignmentFlag.AlignLeading
            | Qt.AlignmentFlag.AlignLeft
        )

        self.horizontalLayout_3.addWidget(self.label_5, 0, Qt.AlignmentFlag.AlignBottom)

        self.frame = QFrame(self.widget)
        self.frame.setObjectName("frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Sunken)
        self.horizontalLayout_6 = QHBoxLayout(self.frame)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.pushButton_7 = QPushButton(self.frame)
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.setMaximumSize(QSize(40, 40))
        icon = QIcon()
        icon.addFile(
            ":/dashboard/icons/bell.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.pushButton_7.setIcon(icon)
        self.pushButton_7.setIconSize(QSize(32, 32))
        self.pushButton_7.setAutoDefault(False)

        self.horizontalLayout_6.addWidget(self.pushButton_7)

        self.horizontalLayout_3.addWidget(self.frame)

        self.ProfileButton = QProfileButton(self.widget)
        self.ProfileButton.setObjectName("ProfileButton")
        sizePolicy.setHeightForWidth(
            self.ProfileButton.sizePolicy().hasHeightForWidth()
        )
        self.ProfileButton.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.ProfileButton)

        self.label_6 = QLabel(self.widget)
        self.label_6.setObjectName("label_6")
        font2 = QFont()
        font2.setFamilies(["Inclusive Sans"])
        font2.setPointSize(14)
        self.label_6.setFont(font2)

        self.horizontalLayout_3.addWidget(self.label_6)

        self.verticalLayout.addWidget(self.widget)

        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName("widget_2")
        sizePolicy2 = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy2)
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_3 = QWidget(self.widget_2)
        self.widget_3.setObjectName("widget_3")
        self.widget_3.setMaximumSize(QSize(300, 1115))
        self.widget_3.setAutoFillBackground(False)
        self.widget_3.setStyleSheet("")
        self.verticalLayout_6 = QVBoxLayout(self.widget_3)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.widget_11 = QWidget(self.widget_3)
        self.widget_11.setObjectName("widget_11")
        sizePolicy3 = QSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.widget_11.sizePolicy().hasHeightForWidth())
        self.widget_11.setSizePolicy(sizePolicy3)
        self.widget_11.setAutoFillBackground(False)
        self.widget_11.setStyleSheet(
            "QPushButton {\n"
            "	background-color: #D9D9D9;\n"
            "	color: black;\n"
            "	font-size: 20px\n"
            "}"
        )
        self.verticalLayout_7 = QVBoxLayout(self.widget_11)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.widget_12 = QWidget(self.widget_11)
        self.widget_12.setObjectName("widget_12")
        sizePolicy4 = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed
        )
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.widget_12.sizePolicy().hasHeightForWidth())
        self.widget_12.setSizePolicy(sizePolicy4)
        self.widget_12.setAutoFillBackground(False)
        self.widget_12.setStyleSheet("")
        self.verticalLayout_8 = QVBoxLayout(self.widget_12)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.pushButton = QPushButton(self.widget_12)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setMinimumSize(QSize(150, 50))
        font3 = QFont()
        font3.setFamilies(["Roboto"])
        self.pushButton.setFont(font3)
        icon1 = QIcon()
        icon1.addFile(
            ":/dashboard/icons/clipboard.svg",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.pushButton.setIcon(icon1)
        self.pushButton.setIconSize(QSize(32, 32))

        self.verticalLayout_8.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.widget_12)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(150, 50))
        self.pushButton_2.setFont(font3)
        icon2 = QIcon()
        icon2.addFile(
            ":/dashboard/icons/user.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.pushButton_2.setIcon(icon2)
        self.pushButton_2.setIconSize(QSize(32, 32))

        self.verticalLayout_8.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.widget_12)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(150, 50))
        self.pushButton_3.setFont(font3)
        icon3 = QIcon()
        icon3.addFile(
            ":/dashboard/icons/money-from-bracket.svg",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.pushButton_3.setIcon(icon3)
        self.pushButton_3.setIconSize(QSize(32, 32))

        self.verticalLayout_8.addWidget(self.pushButton_3)

        self.pushButton_4 = QPushButton(self.widget_12)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setMinimumSize(QSize(150, 50))
        self.pushButton_4.setFont(font3)
        self.pushButton_4.setAutoFillBackground(False)
        icon4 = QIcon()
        icon4.addFile(
            ":/dashboard/icons/clock", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.pushButton_4.setIcon(icon4)
        self.pushButton_4.setIconSize(QSize(32, 32))

        self.verticalLayout_8.addWidget(self.pushButton_4)

        self.pushButton_5 = QPushButton(self.widget_12)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setMinimumSize(QSize(150, 50))
        self.pushButton_5.setFont(font3)
        self.pushButton_5.setStyleSheet("")
        icon5 = QIcon()
        icon5.addFile(
            ":/dashboard/icons/support-svgrepo-com.svg",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.pushButton_5.setIcon(icon5)
        self.pushButton_5.setIconSize(QSize(32, 32))

        self.verticalLayout_8.addWidget(self.pushButton_5)

        self.verticalLayout_7.addWidget(self.widget_12)

        self.widget_13 = QWidget(self.widget_11)
        self.widget_13.setObjectName("widget_13")
        self.verticalLayout_9 = QVBoxLayout(self.widget_13)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.pushButton_6 = QPushButton(self.widget_13)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.setMinimumSize(QSize(150, 35))
        self.pushButton_6.setFont(font3)
        icon6 = QIcon()
        icon6.addFile(
            ":/dashboard/icons/gear.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.pushButton_6.setIcon(icon6)
        self.pushButton_6.setIconSize(QSize(32, 32))

        self.verticalLayout_9.addWidget(self.pushButton_6)

        self.verticalLayout_7.addWidget(self.widget_13, 0, Qt.AlignmentFlag.AlignBottom)

        self.verticalLayout_6.addWidget(self.widget_11)

        self.horizontalLayout.addWidget(self.widget_3)

        self.contentStackedWidget = QStackedWidget(self.widget_2)
        self.contentStackedWidget.setObjectName("contentStackedWidget")
        self.page = QWidget()
        self.page.setObjectName("page")
        self.contentStackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName("page_2")
        self.contentStackedWidget.addWidget(self.page_2)

        self.horizontalLayout.addWidget(self.contentStackedWidget)

        self.verticalLayout.addWidget(self.widget_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 646, 30))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.pushButton_7.setDefault(False)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "MainWindow", None)
        )
        self.label_7.setText("")
        self.label.setText(
            QCoreApplication.translate("MainWindow", "BankOps Banking", None)
        )
        self.label_5.setText(
            QCoreApplication.translate("MainWindow", "Banking done the right way", None)
        )
        self.pushButton_7.setText("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", "John Doe", None))
        self.pushButton.setText(
            QCoreApplication.translate("MainWindow", "Dashboard", None)
        )
        self.pushButton_2.setText(
            QCoreApplication.translate("MainWindow", "Accounts", None)
        )
        self.pushButton_3.setText(
            QCoreApplication.translate("MainWindow", "Transactions", None)
        )
        self.pushButton_4.setText(
            QCoreApplication.translate("MainWindow", "Bill Payments", None)
        )
        # if QT_CONFIG(tooltip)
        self.pushButton_5.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.pushButton_5.setText(
            QCoreApplication.translate("MainWindow", "Support", None)
        )
        self.pushButton_6.setText(
            QCoreApplication.translate("MainWindow", "Settings", None)
        )

    # retranslateUi
