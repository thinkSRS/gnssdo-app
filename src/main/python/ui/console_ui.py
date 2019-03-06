# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'console_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.console_history = QtWidgets.QTextEdit(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.console_history.setFont(font)
        self.console_history.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.console_history.setReadOnly(True)
        self.console_history.setObjectName("console_history")
        self.verticalLayout.addWidget(self.console_history)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.console_cmd = HistoryLineEdit(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.console_cmd.setFont(font)
        self.console_cmd.setObjectName("console_cmd")
        self.verticalLayout.addWidget(self.console_cmd)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Command History"))
        self.label_2.setText(_translate("Form", "Send Command"))

from history_lineedit import HistoryLineEdit
