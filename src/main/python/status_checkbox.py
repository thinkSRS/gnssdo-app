# Copyright: Stanford Reserach Systems, Inc and contributors
# License: GNU GPL, version 3 or later; https://www.gnu.org/licenses/gpl-3.0.html
"""Simulates a status led"""
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


class StatusCheckBox(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.NoFocus)
        self.style_str_off = "QCheckBox::disabled { color : gray; }"
        self.style_format_str_on = "QCheckBox::disabled {{ color : gray; }}" \
                                   "QCheckBox::indicator::enabled {{ background-color : rgba({0},{1},{2},255); }}" \
                                   "QCheckBox::indicator::disabled {{ background-color : rgba({0},{1},{2},64); }}"
        self.asserted = False
        self.color = QColor(0, 0, 255)
        self._update()

    def set_color(self, color):
        self.color = color
        self._update()

    def set_led(self, led_on):
        self.asserted = led_on
        self._update()

    def _update(self):
        if self.asserted:
            style_text = self.style_format_str_on.format(self.color.red(), self.color.green(), self.color.blue())
        else:
            style_text = self.style_str_off
        self.setStyleSheet(style_text)

    def keyPressEvent(self, event):
        pass

    def keyReleaseEvent(self, event):
        pass

    def mousePressEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass
