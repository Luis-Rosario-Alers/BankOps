# -*- coding: utf-8 -*-
from PySide6.QtCore import (
    QCoreApplication,
    QMetaObject,
    QSize,
    Qt,
)
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Ui_transactions(object):
    def setupUi(self, transactions):
        if not transactions.objectName():
            transactions.setObjectName("transactions")
        transactions.resize(990, 619)
        self.horizontalLayout = QHBoxLayout(transactions)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.transactionFormContainerWidget = QWidget(transactions)
        self.transactionFormContainerWidget.setObjectName(
            "transactionFormContainerWidget"
        )
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.transactionFormContainerWidget.sizePolicy().hasHeightForWidth()
        )
        self.transactionFormContainerWidget.setSizePolicy(sizePolicy)
        self.transactionFormContainerWidget.setMaximumSize(QSize(500, 16777215))
        self.verticalLayout = QVBoxLayout(self.transactionFormContainerWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.transactionInputFormsContainerWidget = QWidget(
            self.transactionFormContainerWidget
        )
        self.transactionInputFormsContainerWidget.setObjectName(
            "transactionInputFormsContainerWidget"
        )
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.transactionInputFormsContainerWidget.sizePolicy().hasHeightForWidth()
        )
        self.transactionInputFormsContainerWidget.setSizePolicy(sizePolicy1)
        self.verticalLayout_2 = QVBoxLayout(self.transactionInputFormsContainerWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.transactionTypeContainerWidget = QWidget(
            self.transactionInputFormsContainerWidget
        )
        self.transactionTypeContainerWidget.setObjectName(
            "transactionTypeContainerWidget"
        )
        sizePolicy1.setHeightForWidth(
            self.transactionTypeContainerWidget.sizePolicy().hasHeightForWidth()
        )
        self.transactionTypeContainerWidget.setSizePolicy(sizePolicy1)
        self.horizontalLayout_3 = QHBoxLayout(self.transactionTypeContainerWidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.transactionTypeLabel = QLabel(self.transactionTypeContainerWidget)
        self.transactionTypeLabel.setObjectName("transactionTypeLabel")

        self.horizontalLayout_3.addWidget(self.transactionTypeLabel)

        self.transactionTypeLineEdit = QLineEdit(self.transactionTypeContainerWidget)
        self.transactionTypeLineEdit.setObjectName("transactionTypeLineEdit")

        self.horizontalLayout_3.addWidget(self.transactionTypeLineEdit)

        self.verticalLayout_2.addWidget(self.transactionTypeContainerWidget)

        self.transactionAmountContainerWidget = QWidget(
            self.transactionInputFormsContainerWidget
        )
        self.transactionAmountContainerWidget.setObjectName(
            "transactionAmountContainerWidget"
        )
        sizePolicy1.setHeightForWidth(
            self.transactionAmountContainerWidget.sizePolicy().hasHeightForWidth()
        )
        self.transactionAmountContainerWidget.setSizePolicy(sizePolicy1)
        self.horizontalLayout_2 = QHBoxLayout(self.transactionAmountContainerWidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.transactionAmountLabel = QLabel(self.transactionAmountContainerWidget)
        self.transactionAmountLabel.setObjectName("transactionAmountLabel")

        self.horizontalLayout_2.addWidget(self.transactionAmountLabel)

        self.transactionAmountLineEdit = QLineEdit(
            self.transactionAmountContainerWidget
        )
        self.transactionAmountLineEdit.setObjectName("transactionAmountLineEdit")

        self.horizontalLayout_2.addWidget(self.transactionAmountLineEdit)

        self.verticalLayout_2.addWidget(self.transactionAmountContainerWidget)

        self.verticalLayout.addWidget(self.transactionInputFormsContainerWidget)

        self.transactionPromptsContainerWidget = QWidget(
            self.transactionFormContainerWidget
        )
        self.transactionPromptsContainerWidget.setObjectName(
            "transactionPromptsContainerWidget"
        )
        self.verticalLayout_3 = QVBoxLayout(self.transactionPromptsContainerWidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.transactionConfirmContainerWidget = QWidget(
            self.transactionPromptsContainerWidget
        )
        self.transactionConfirmContainerWidget.setObjectName(
            "transactionConfirmContainerWidget"
        )
        self.verticalLayout_4 = QVBoxLayout(self.transactionConfirmContainerWidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.transactionConfirmPushButton = QPushButton(
            self.transactionConfirmContainerWidget
        )
        self.transactionConfirmPushButton.setObjectName("transactionConfirmPushButton")

        self.verticalLayout_4.addWidget(self.transactionConfirmPushButton)

        self.verticalLayout_3.addWidget(
            self.transactionConfirmContainerWidget, 0, Qt.AlignmentFlag.AlignTop
        )

        self.verticalLayout.addWidget(self.transactionPromptsContainerWidget)

        self.horizontalLayout.addWidget(self.transactionFormContainerWidget)

        self.transactionContainerWidget = QWidget(transactions)
        self.transactionContainerWidget.setObjectName("transactionContainerWidget")
        self.verticalLayout_5 = QVBoxLayout(self.transactionContainerWidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.transactionTablePlaceholderLabel = QLabel(self.transactionContainerWidget)
        self.transactionTablePlaceholderLabel.setObjectName(
            "transactionTablePlaceholderLabel"
        )
        self.transactionTablePlaceholderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.transactionTablePlaceholderLabel)

        self.horizontalLayout.addWidget(self.transactionContainerWidget)

        self.retranslateUi(transactions)

        QMetaObject.connectSlotsByName(transactions)

    # setupUi

    def retranslateUi(self, transactions):
        transactions.setWindowTitle(
            QCoreApplication.translate("transactions", "Form", None)
        )
        self.transactionTypeLabel.setText(
            QCoreApplication.translate("transactions", "Transaction type", None)
        )
        self.transactionAmountLabel.setText(
            QCoreApplication.translate("transactions", "Amount", None)
        )
        self.transactionConfirmPushButton.setText(
            QCoreApplication.translate("transactions", "Confirm", None)
        )
        self.transactionTablePlaceholderLabel.setText(
            QCoreApplication.translate("transactions", "Transaction Table Widget", None)
        )

    # retranslateUi
