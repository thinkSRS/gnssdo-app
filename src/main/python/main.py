# Copyright: Stanford Reserach Systems, Inc and contributors
# License: GNU GPL, version 3 or later; https://www.gnu.org/licenses/gpl-3.0.html
import sys

from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox)
from PyQt5.QtSerialPort import QSerialPortInfo
from PyQt5.QtCore import (QThread, QCoreApplication, QSettings, QSize, QPoint)
from fbs_runtime.application_context import ApplicationContext

import commthread
from ui import mainwindow


class GnssdoMainWindow(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connected = False
        self.workerthread = QThread()
        self.worker = commthread.CommThread()
        self.worker.moveToThread(self.workerthread)
        QCoreApplication.setOrganizationName("Stanford Research Systems")
        QCoreApplication.setOrganizationDomain("thinksrs.com")
        QCoreApplication.setApplicationName("GnssDO App")
        # Restore user size and position
        settings = QSettings()
        self.resize(settings.value("window_size", QSize(700, 600)))
        self.move(settings.value("window_pos", QPoint(80, 80)))
        self.populate_comport_combobox(settings.value("comport", "Select"))
        self.connect_btn.clicked.connect(self.on_connect)
        self.main_tab_ctrl.currentChanged.connect(self.on_tab_changed)
        self.update_connect_btn_text()
        # Start up worker thread
        self.launch_workerthread()

    def closeEvent(self, event):
        # Signal worker thread to break out of infinite loop
        self.worker.set_mode(commthread.ModeEnum.MODE_QUIT)
        # Save settings
        settings = QSettings()
        settings.setValue("window_size", self.size())
        settings.setValue("window_pos", self.pos())
        settings.setValue("comport", self.comport_combobox.currentText())
        # Shut down thread's event loop and wait for thread terminate
        self.workerthread.quit()
        self.workerthread.wait(500)
        super().closeEvent(event)

    def populate_comport_combobox(self, default_port=None):
        # Make sure we at least have a select item
        if 0 == self.comport_combobox.count():
            self.comport_combobox.insertItem(0, "Select")
        # Remove all old items
        while self.comport_combobox.count() > 1:
            self.comport_combobox.removeItem(1)
        # Repopulate with fresh list of available COM ports
        port_name_list = [port.portName() for port in QSerialPortInfo.availablePorts()]
        port_name_list.sort()
        for index, port_name in enumerate(port_name_list):
            self.comport_combobox.insertItem(index + 1, port_name)
        # Select the default item if it exists
        if default_port:
            default_index = self.comport_combobox.findText(default_port)
            if -1 == default_index:
                default_index = 0
            self.comport_combobox.setCurrentIndex(default_index)

    def update_connect_btn_text(self):
        btn_text = "Disconnect" if self.connected else "Connect"
        self.connect_btn.setText(btn_text)
        for tab in range(self.main_tab_ctrl.count()):
            self.main_tab_ctrl.widget(tab).setEnabled(self.connected)

    def launch_workerthread(self):
        self.worker.data_signal.connect(self.gpsstatus_widget.on_gps_data)
        self.worker.setup_signal.connect(self.gpssetup_widget.on_gps_setup)
        self.worker.error_signal.connect(self.on_error)
        self.worker.receive_signal.connect(self.console_widget.on_receive_data)
        self.worker.disconnect_signal.connect(self.on_disconnected)
        self.console_widget.send_data_signal.connect(self.worker.send_command)
        self.gpsstatus_widget.send_data_signal.connect(self.worker.send_command)
        self.gpssetup_widget.send_data_signal.connect(self.worker.send_command)
        self.workerthread.started.connect(self.worker.work)
        self.workerthread.finished.connect(self.on_thread_finished)
        self.workerthread.start()

    def on_connect(self):
        if self.connected:
            # Request to disconnect from serial port
            self.worker.connect(False)
        elif self.valid_comport():
            # Request connection to serial port
            self.worker.set_serial_port(self.comport_combobox.currentText())
            self.worker.connect(True)
            self.connected = True
        else:
            QMessageBox.warning(self, 'Error', "Please select a communications port")
        self.update_connect_btn_text()

    def valid_comport(self):
        current_text = self.comport_combobox.currentText()
        self.populate_comport_combobox(current_text)
        return self.comport_combobox.currentIndex() > 0

    def on_disconnected(self):
        self.connected = False
        self.update_connect_btn_text()

    def on_tab_changed(self, index):
        if 1 == index:
            self.worker.set_mode(commthread.ModeEnum.MODE_SETUP)
        elif 2 == index:
            self.worker.set_mode(commthread.ModeEnum.MODE_CONSOLE)
            self.console_widget.console_cmd.setFocus()
        else:
            self.worker.set_mode(commthread.ModeEnum.MODE_STATUS)

    def on_thread_finished(self):
        pass

    def on_error(self, error):
        QMessageBox.critical(self, 'Error', str(error))


class AppContext(ApplicationContext):
    def run(self):
        window = GnssdoMainWindow()
        version = self.build_settings['version']
        window.setWindowTitle("GnssDO App v" + version)
        window.show()
        return self.app.exec_()


if __name__ == '__main__':
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)
