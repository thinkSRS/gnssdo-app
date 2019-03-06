# Copyright: Stanford Reserach Systems, Inc and contributors
# License: GNU GPL, version 3 or later; https://www.gnu.org/licenses/gpl-3.0.html
"""LineEdit component with command history"""
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import (Qt, pyqtSignal)


class HistoryLineEdit(QLineEdit):
    cmd_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.textChanged.connect(self.on_text_changed)
        self.cmd_history = []
        self.cmd_history_index = -1

    def keyPressEvent(self, event):
        key = event.key()
        if Qt.Key_Up == key:
            if len(self.cmd_history):
                if -1 == self.cmd_history_index:
                    self.cmd_history_index = len(self.cmd_history) - 1
                elif self.cmd_history_index > 0:
                    self.cmd_history_index -= 1
                self.setText(self.cmd_history[self.cmd_history_index])
        elif Qt.Key_Down == key:
            length = len(self.cmd_history)
            if length:
                if -1 == self.cmd_history_index:
                    self.clear()
                elif self.cmd_history_index < length:
                    self.cmd_history_index += 1
                    if self.cmd_history_index == length:
                        self.cmd_history_index = -1
                        self.clear()
                    else:
                        self.setText(self.cmd_history[self.cmd_history_index])
        elif Qt.Key_Return == key:
            text = self.normalize_newlines(self.text())
            # Append unique commands to the history of commands
            if not len(self.cmd_history) or text != self.cmd_history[-1]:
                self.cmd_history.append(text)
            self.cmd_history_index = -1
            self.clear()
            self.cmd_signal.emit(text)
        else:
            super().keyPressEvent(event)

    def on_text_changed(self):
        text = self.text()
        index_newline = text.rfind("\n")
        if -1 != index_newline:
            send_text = self.normalize_newlines(text[0:index_newline+1])
            new_text = text[index_newline+1:]
            self.setText(new_text)
            self.setCursorPosition(len(new_text))
            self.cmd_signal.emit(send_text[0:-1])

    @staticmethod
    def normalize_newlines(text):
        return text.replace("\r\n", "\n")
