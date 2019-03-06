# Copyright: Stanford Reserach Systems, Inc and contributors
# License: GNU GPL, version 3 or later; https://www.gnu.org/licenses/gpl-3.0.html
"""Helper classes for displaying formatted data"""


class DurationDisplay:
    def __init__(self, duration):
        self.duration = duration

    def get(self):
        value = float(self.duration)
        format_str = "%0.2f"
        units = " s"
        if value >= 86400:
            value /= 86400
            units = " day"
        elif value >= 3600:
            value /= 3600
            units = " hr"
        else:
            format_str = "%0.0f"
        text = format_str % value
        text += units
        return text


class AbbrevTimeDisplay:
    def __init__(self, time_value, precision=1):
        self.time_value = time_value
        self.precision = precision

    def get(self):
        format_str = "%%0.%df" % self.precision
        value = self.time_value
        abs_value = abs(value)
        if abs_value < 1e-6:
            format_str += " ns"
            value *= 1e9
        elif abs_value < 1e-3:
            format_str += " us"
            value *= 1e6
        elif abs_value < 1.0:
            format_str += " ms"
            value *= 1e3
        else:
            format_str += " s"
        return format_str % value


class TimeDelayDisplay:
    def __init__(self, time_value, digits=0):
        self.time_value = time_value
        self.digits = digits

    def get(self):
        value = self.time_value
        abs_value = abs(value)
        if abs_value < 1e-6:
            format_str = "%%0.%df ns" % self.digits
            value *= 1e9
        elif abs_value < 1e-3:
            format_str = "%%0.%df us" % (self.digits + 3)
            value *= 1e6
        elif abs_value < 1.0:
            format_str = "%%0.%df ms" % (self.digits + 6)
            value *= 1e3
        else:
            format_str = "%%0.%df s" % (self.digits + 9)
        return format_str % value
