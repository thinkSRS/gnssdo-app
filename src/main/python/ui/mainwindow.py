# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(663, 549)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.horizontal_layout.setSpacing(6)
        self.horizontal_layout.setObjectName("horizontal_layout")
        self.comm_label = QtWidgets.QLabel(self.centralWidget)
        self.comm_label.setObjectName("comm_label")
        self.horizontal_layout.addWidget(self.comm_label)
        self.comport_combobox = QtWidgets.QComboBox(self.centralWidget)
        self.comport_combobox.setCurrentText("")
        self.comport_combobox.setObjectName("comport_combobox")
        self.horizontal_layout.addWidget(self.comport_combobox)
        self.connect_btn = QtWidgets.QPushButton(self.centralWidget)
        self.connect_btn.setObjectName("connect_btn")
        self.horizontal_layout.addWidget(self.connect_btn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontal_layout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontal_layout)
        self.main_tab_ctrl = QtWidgets.QTabWidget(self.centralWidget)
        self.main_tab_ctrl.setEnabled(True)
        self.main_tab_ctrl.setObjectName("main_tab_ctrl")
        self.status_tab = QtWidgets.QWidget()
        self.status_tab.setObjectName("status_tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.status_tab)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gpsstatus_widget = GpsStatusWidget(self.status_tab)
        self.gpsstatus_widget.setObjectName("gpsstatus_widget")
        self.verticalLayout_2.addWidget(self.gpsstatus_widget)
        self.main_tab_ctrl.addTab(self.status_tab, "")
        self.setup_tab = QtWidgets.QWidget()
        self.setup_tab.setObjectName("setup_tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.setup_tab)
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gpssetup_widget = GpsSetupWidget(self.setup_tab)
        self.gpssetup_widget.setObjectName("gpssetup_widget")
        self.verticalLayout_3.addWidget(self.gpssetup_widget)
        self.main_tab_ctrl.addTab(self.setup_tab, "")
        self.console_tab = QtWidgets.QWidget()
        self.console_tab.setObjectName("console_tab")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.console_tab)
        self.verticalLayout_5.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.console_widget = ConsoleWidget(self.console_tab)
        self.console_widget.setObjectName("console_widget")
        self.verticalLayout_5.addWidget(self.console_widget)
        self.main_tab_ctrl.addTab(self.console_tab, "")
        self.verticalLayout.addWidget(self.main_tab_ctrl)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menu_bar = QtWidgets.QMenuBar(MainWindow)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 663, 21))
        self.menu_bar.setObjectName("menu_bar")
        MainWindow.setMenuBar(self.menu_bar)
        self.main_tool_bar = QtWidgets.QToolBar(MainWindow)
        self.main_tool_bar.setObjectName("main_tool_bar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.main_tool_bar)
        self.status_bar = QtWidgets.QStatusBar(MainWindow)
        self.status_bar.setObjectName("status_bar")
        MainWindow.setStatusBar(self.status_bar)

        self.retranslateUi(MainWindow)
        self.main_tab_ctrl.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.comm_label.setText(_translate("MainWindow", "Communications:"))
        self.connect_btn.setText(_translate("MainWindow", "Connect"))
        self.main_tab_ctrl.setTabText(self.main_tab_ctrl.indexOf(self.status_tab), _translate("MainWindow", "Instrument Status"))
        self.main_tab_ctrl.setTabText(self.main_tab_ctrl.indexOf(self.setup_tab), _translate("MainWindow", "Configuration"))
        self.main_tab_ctrl.setTabText(self.main_tab_ctrl.indexOf(self.console_tab), _translate("MainWindow", "Console"))

from console_widget import ConsoleWidget
from gpssetup_widget import GpsSetupWidget
from gpsstatus_widget import GpsStatusWidget
