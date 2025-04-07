from PySide6.QtCore import (
    QCoreApplication,
    QMetaObject,
    Qt,
)
from PySide6.QtGui import (
    QFont,
)
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class Ui_login_window(object):
    def setupUi(self, login_window):
        if not login_window.objectName():
            login_window.setObjectName("login_window")
        login_window.resize(502, 405)
        self.centralwidget = QWidget(login_window)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_6 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.loginContainerWidget = QWidget(self.centralwidget)
        self.loginContainerWidget.setObjectName("loginContainerWidget")
        self.verticalLayout_5 = QVBoxLayout(self.loginContainerWidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.loginContainerFrameWidget = QFrame(self.loginContainerWidget)
        self.loginContainerFrameWidget.setObjectName("loginContainerFrameWidget")
        font = QFont()
        font.setFamilies(["Yu Gothic"])
        self.loginContainerFrameWidget.setFont(font)
        self.loginContainerFrameWidget.setFrameShape(QFrame.Shape.StyledPanel)
        self.loginContainerFrameWidget.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.loginContainerFrameWidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.loginLabel = QLabel(self.loginContainerFrameWidget)
        self.loginLabel.setObjectName("loginLabel")
        font1 = QFont()
        font1.setFamilies(["Yu Gothic"])
        font1.setPointSize(20)
        self.loginLabel.setFont(font1)
        self.loginLabel.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )

        self.verticalLayout_4.addWidget(
            self.loginLabel,
            0,
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
        )

        self.verticalLayout_5.addWidget(
            self.loginContainerFrameWidget,
            0,
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
        )

        self.verticalLayout_2.addWidget(self.loginContainerWidget)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.authenticateContainerWidget = QWidget(self.centralwidget)
        self.authenticateContainerWidget.setObjectName("authenticateContainerWidget")
        self.verticalLayout = QVBoxLayout(self.authenticateContainerWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.accountNumberContainerWidget = QWidget(self.authenticateContainerWidget)
        self.accountNumberContainerWidget.setObjectName("accountNumberContainerWidget")
        self.horizontalLayout = QHBoxLayout(self.accountNumberContainerWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.accountNumberLabel = QLabel(self.accountNumberContainerWidget)
        self.accountNumberLabel.setObjectName("accountNumberLabel")

        self.horizontalLayout.addWidget(self.accountNumberLabel)

        self.accountNumberLineEdit = QLineEdit(self.accountNumberContainerWidget)
        self.accountNumberLineEdit.setObjectName("accountNumberLineEdit")

        self.horizontalLayout.addWidget(self.accountNumberLineEdit)

        self.verticalLayout.addWidget(self.accountNumberContainerWidget)

        self.pinContainerWidget = QWidget(self.authenticateContainerWidget)
        self.pinContainerWidget.setObjectName("pinContainerWidget")
        self.horizontalLayout_2 = QHBoxLayout(self.pinContainerWidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pinLabel = QLabel(self.pinContainerWidget)
        self.pinLabel.setObjectName("pinLabel")

        self.horizontalLayout_2.addWidget(self.pinLabel)

        self.pinLineEdit = QLineEdit(self.pinContainerWidget)
        self.pinLineEdit.setObjectName("pinLineEdit")

        self.horizontalLayout_2.addWidget(self.pinLineEdit)

        self.verticalLayout.addWidget(self.pinContainerWidget)

        self.authenticatePushButton = QPushButton(self.authenticateContainerWidget)
        self.authenticatePushButton.setObjectName("authenticatePushButton")
        font2 = QFont()
        font2.setFamilies(["Yu Gothic"])
        font2.setPointSize(15)
        self.authenticatePushButton.setFont(font2)

        self.verticalLayout.addWidget(self.authenticatePushButton)

        self.verticalLayout_2.addWidget(self.authenticateContainerWidget)

        self.verticalLayout_6.addLayout(self.verticalLayout_2)

        login_window.setCentralWidget(self.centralwidget)

        self.retranslateUi(login_window)

        QMetaObject.connectSlotsByName(login_window)

    # setupUi

    def retranslateUi(self, login_window):
        login_window.setWindowTitle(
            QCoreApplication.translate("login_window", "Login", None)
        )
        self.loginLabel.setText(
            QCoreApplication.translate("login_window", "Login", None)
        )
        self.accountNumberLabel.setText(
            QCoreApplication.translate("login_window", "Account number:", None)
        )
        self.pinLabel.setText(QCoreApplication.translate("login_window", "PIN:", None))
        self.authenticatePushButton.setText(
            QCoreApplication.translate("login_window", "Authenticate", None)
        )

    # retranslateUi
