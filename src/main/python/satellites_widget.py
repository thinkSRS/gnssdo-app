# Copyright: Stanford Reserach Systems, Inc and contributors
# License: GNU GPL, version 3 or later; https://www.gnu.org/licenses/gpl-3.0.html
"""Special Widget to Paint Satellites"""
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import (QPainter, QColor, QBrush, QFontMetrics)
import math


class SatellitesWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.satellites_used = []
        self.satellites_tracked = []
        self.colors = {}

    def set_colors(self, colors):
        self.colors = colors

    def get_color(self, color_str):
        return self.colors.get(color_str, QColor(240, 0, 0))

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # Get coordinates for the window
        size_window = self.size()
        xcenter = size_window.width() // 2
        ycenter = size_window.height() // 2
        font = painter.font()
        metrics = QFontMetrics(font)
        font_height = metrics.capHeight()
        width_n = metrics.width("N")
        width_s = metrics.width("S")
        width_w = metrics.width("W")
        width_e = metrics.width("E")
        extent = min(size_window.width() - width_w - width_e, size_window.height() - 2 * font_height)
        # Draw labels
        painter.drawText(xcenter - width_n // 2, ycenter - extent // 2, "N")
        painter.drawText(xcenter - width_s // 2, ycenter + extent // 2 + font_height, "S")
        painter.drawText(xcenter - extent // 2 - width_w + 2, ycenter + font_height // 2, "W")
        painter.drawText(xcenter + extent // 2, ycenter + font_height // 2, "E")
        # Draw coordinate system
        diameter = extent - 8
        radius = diameter // 2
        painter.drawEllipse(xcenter - radius, ycenter - radius, diameter, diameter)
        diameter23 = diameter * 2 // 3
        radius23 = diameter23 // 2
        painter.drawEllipse(xcenter - radius23, ycenter - radius23, diameter23, diameter23)
        diameter13 = diameter // 3
        radius13 = diameter13 // 2
        painter.drawEllipse(xcenter - radius13, ycenter - radius13, diameter13, diameter13)
        # Draw satellites
        brushGps = QBrush(self.get_color("blue"))
        brushGlonass = QBrush(self.get_color("red"))
        brushBeidou = QBrush(self.get_color("orange"))
        brushGalileo = QBrush(self.get_color("green"))
        sat_radius = 7
        for sat in self.satellites_tracked:
            # Make radius linear in elevation
            if sat.sv_number in self.satellites_used:
                r = radius * (180 - 2 * sat.elevation) // 180
                if r < 0:
                    r = 0
                x = xcenter + int(r * math.sin(sat.azimuth * math.pi / 180.0))
                y = ycenter - int(r * math.cos(sat.azimuth * math.pi / 180.0))
                if 1*64 <= sat.sv_number < 2*64:
                    brush = brushGlonass
                elif 2*64 <= sat.sv_number < 3*64:
                    brush = brushBeidou
                elif 3*64 <= sat.sv_number < 4*64:
                    brush = brushGalileo
                else:
                    brush = brushGps
                painter.setBrush(brush)
                painter.drawEllipse(x - sat_radius // 2, y - sat_radius // 2, sat_radius, sat_radius)
        painter.end()

    def set_satellites(self, satellites_used, satellites_tracked):
        self.satellites_used = satellites_used
        self.satellites_tracked = satellites_tracked
        self.update()
