# Copyright: Stanford Reserach Systems, Inc and contributors
# License: GNU GPL, version 3 or later; https://www.gnu.org/licenses/gpl-3.0.html
"""A read only checkbox"""
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import Qt


class ReadOnlyCheckBox(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.NoFocus)

    def keyPressEvent(self, event):
        pass

    def keyReleaseEvent(self, event):
        pass

    def mousePressEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass
