# Copyright: Stanford Reserach Systems, Inc and contributors
# License: GNU GPL, version 3 or later; https://www.gnu.org/licenses/gpl-3.0.html
"""Console for sending commands to Gpsdo manually"""
from PyQt5.QtCore import (pyqtSignal)
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import (QTextCursor, QFont, QColor)

from ui import console_ui


class ConsoleWidget(QWidget, console_ui.Ui_Form):
    send_data_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        # Call Qt Designer setup code
        self.setupUi(self)
        self.send_appender = SendAppendHelper(self.console_history)
        self.receive_appender = ReceiveAppendHelper(self.console_history)
        self.console_history.setPlaceholderText("Enter commands below")
        self.console_cmd.cmd_signal.connect(self.on_console_command)

    def on_console_command(self, text):
        self.send_appender.append(text + "\n")
        self.send_data_signal.emit(text)

    def on_receive_data(self, text):
        receive_text = self.normalize_newlines(text)
        append_helper = ReceiveAppendHelper(self.console_history)
        append_helper.append(receive_text)

    @staticmethod
    def normalize_newlines(text):
        return text.replace("\r\n", "\n")


class AppendEditHelper:
    def __init__(self, edit, color, weight):
        self.edit = edit
        self.color = color
        self.weight = weight

    def append(self, text):
        self.edit.moveCursor(QTextCursor.End, QTextCursor.MoveAnchor)
        self.edit.setTextColor(self.color)
        self.edit.setFontWeight(self.weight)
        self.edit.insertPlainText(text)
        self.edit.moveCursor(QTextCursor.End, QTextCursor.MoveAnchor)


class SendAppendHelper(AppendEditHelper):
    def __init__(self, edit):
        super().__init__(edit, QColor(0, 0, 255), QFont.Bold)


class ReceiveAppendHelper(AppendEditHelper):
    def __init__(self, edit):
        super().__init__(edit, QColor(0, 0, 0), QFont.Normal)
