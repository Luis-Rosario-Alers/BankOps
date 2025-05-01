from PySide6.QtCore import (
    QCoreApplication,
    QMetaObject,
    QSize,
    Qt,
)
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Ui_Dashboard(object):
    def setupUi(self, Dashboard):
        if not Dashboard.objectName():
            Dashboard.setObjectName("Dashboard")
        Dashboard.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Dashboard)
        self.verticalLayout.setObjectName("verticalLayout")
        self.dashboard_background = QWidget(Dashboard)
        self.dashboard_background.setObjectName("dashboard_background")
        self.dashboard_background.setSizeIncrement(QSize(0, 0))
        self.verticalLayout_3 = QVBoxLayout(self.dashboard_background)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget_5 = QWidget(self.dashboard_background)
        self.widget_5.setObjectName("widget_5")
        self.widget_5.setStyleSheet("")
        self.verticalLayout_4 = QVBoxLayout(self.widget_5)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widget_7 = QWidget(self.widget_5)
        self.widget_7.setObjectName("widget_7")
        self.verticalLayout_5 = QVBoxLayout(self.widget_7)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_3 = QLabel(self.widget_7)
        self.label_3.setObjectName("label_3")

        self.verticalLayout_5.addWidget(self.label_3, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout_4.addWidget(self.widget_7, 0, Qt.AlignmentFlag.AlignTop)

        self.widget_8 = QWidget(self.widget_5)
        self.widget_8.setObjectName("widget_8")
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_8.sizePolicy().hasHeightForWidth())
        self.widget_8.setSizePolicy(sizePolicy)
        self.horizontalLayout_7 = QHBoxLayout(self.widget_8)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")

        self.verticalLayout_4.addWidget(self.widget_8)

        self.verticalLayout_3.addWidget(self.widget_5)

        self.widget_6 = QWidget(self.dashboard_background)
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widget_9 = QWidget(self.widget_6)
        self.widget_9.setObjectName("widget_9")
        self.verticalLayout_10 = QVBoxLayout(self.widget_9)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.widget_14 = QWidget(self.widget_9)
        self.widget_14.setObjectName("widget_14")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_14)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QLabel(self.widget_14)
        self.label_2.setObjectName("label_2")

        self.horizontalLayout_4.addWidget(
            self.label_2, 0, Qt.AlignmentFlag.AlignHCenter
        )

        self.verticalLayout_10.addWidget(self.widget_14, 0, Qt.AlignmentFlag.AlignTop)

        self.widget_15 = QWidget(self.widget_9)
        self.widget_15.setObjectName("widget_15")
        sizePolicy.setHeightForWidth(self.widget_15.sizePolicy().hasHeightForWidth())
        self.widget_15.setSizePolicy(sizePolicy)

        self.verticalLayout_10.addWidget(self.widget_15)

        self.horizontalLayout_2.addWidget(self.widget_9)

        self.widget_10 = QWidget(self.widget_6)
        self.widget_10.setObjectName("widget_10")
        self.verticalLayout_2 = QVBoxLayout(self.widget_10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_16 = QWidget(self.widget_10)
        self.widget_16.setObjectName("widget_16")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_16)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QLabel(self.widget_16)
        self.label_4.setObjectName("label_4")

        self.horizontalLayout_5.addWidget(
            self.label_4, 0, Qt.AlignmentFlag.AlignHCenter
        )

        self.verticalLayout_2.addWidget(self.widget_16, 0, Qt.AlignmentFlag.AlignTop)

        self.widget_17 = QWidget(self.widget_10)
        self.widget_17.setObjectName("widget_17")
        sizePolicy.setHeightForWidth(self.widget_17.sizePolicy().hasHeightForWidth())
        self.widget_17.setSizePolicy(sizePolicy)
        self.verticalLayout_14 = QVBoxLayout(self.widget_17)
        self.verticalLayout_14.setObjectName("verticalLayout_14")

        self.verticalLayout_2.addWidget(self.widget_17)

        self.horizontalLayout_2.addWidget(self.widget_10)

        self.verticalLayout_3.addWidget(self.widget_6)

        self.verticalLayout.addWidget(self.dashboard_background)

        self.retranslateUi(Dashboard)

        QMetaObject.connectSlotsByName(Dashboard)

    # setupUi

    def retranslateUi(self, Dashboard):
        Dashboard.setWindowTitle(
            QCoreApplication.translate("Dashboard", "Dashboard", None)
        )
        self.label_3.setText(QCoreApplication.translate("Dashboard", "Summary", None))
        self.label_2.setText(QCoreApplication.translate("Dashboard", "Accounts", None))
        self.label_4.setText(
            QCoreApplication.translate("Dashboard", "Latest transactions", None)
        )

    # retranslateUi
