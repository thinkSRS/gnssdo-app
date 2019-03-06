# Copyright: Stanford Reserach Systems, Inc and contributors
# License: GNU GPL, version 3 or later; https://www.gnu.org/licenses/gpl-3.0.html
"""GpsStatusWidget for displaying Gpsdo status"""
import math

from PyQt5.QtCore import (QTimer, pyqtSignal)
from PyQt5.QtWidgets import (QWidget, QMessageBox)
from PyQt5.QtGui import QColor

from ui import gpsstatus_ui
from data_display import (DurationDisplay, AbbrevTimeDisplay)


class GpsStatusWidget(QWidget, gpsstatus_ui.Ui_Form):
    send_data_signal = pyqtSignal(str)

    timebase_state_desc = {
        "NON": "None",
        "POW": "Warming up",
        "SEAR": "Searching for sat.",
        "STAB": "Stabilizing",
        "VTIM": "Validating time",
        "LOCK": "Locked",
        "MAN": "Holdover, manual",
        "NGPS": "Holdover, no 1pps",
        "BGPS": "Holdover, bad timing"
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        # Call Qt Designer setup code
        self.setupUi(self)
        self.model = "FS752"
        self.version = 0.50
        self.colors = {}
        self.init_colors()
        self.init_status_leds()
        self.init_legend_leds()
        self.satellites_widget.set_colors(self.colors)
        self.event_clear_btn.clicked.connect(self.on_event_clear)
        self.alarm_clear_btn.clicked.connect(self.on_alarm_clear)
        self.alarm_clear_btn.hide()
        self.restart_btn.clicked.connect(self.on_restart_survey)
        self.alarm_mode = "TRAC"
        self.alarm = 0

    def isOldFS740(self):
        return "FS740" == self.model and self.version < 4.00

    def init_colors(self):
        self.colors["orange"] = QColor(240, 150, 0)
        self.colors["red"] = QColor(240, 0, 0)
        self.colors["green"] = QColor(0, 200, 0)
        self.colors["blue"] = QColor(0, 128, 255)
        self.colors["yellow"] = QColor(255, 255, 0)

    def init_status_leds(self):
        orange = self.colors["orange"]
        self.notime_led.set_color(orange)
        self.antopen_led.set_color(orange)
        self.antshort_led.set_color(orange)
        self.nosat_led.set_color(orange)
        self.utc_led.set_color(orange)
        self.survey_led.set_color(orange)
        self.leapsec_led.set_color(orange)
        green = self.colors["green"]
        self.locked_led.set_color(green)
        self.stable_led.set_color(green)
        red = self.colors["red"]
        self.holdover_led.set_color(red)

    def init_legend_leds(self):
        self.legend_gps.set_color(self.colors["blue"])
        self.legend_glonass.set_color(self.colors["red"])
        self.legend_beidou.set_color(self.colors["orange"])
        self.legend_galileo.set_color(self.colors["green"])
        self.legend_gps.set_led(True)
        self.legend_glonass.set_led(True)
        self.legend_beidou.set_led(True)
        self.legend_galileo.set_led(True)

    def on_gps_data(self, data):
        self.serial = data.serial
        self.model = data.model
        self.version = float(data.version[0:4])
        self.update_postion(data)
        self.update_satellites(data)
        self.update_utc(data)
        self.update_gps_status(data)
        self.update_timebase(data)
        self.update_events(data)
        self.update_alarm(data)

    def on_event_clear(self):
        if self.isOldFS740():
            self.send_data_signal.emit("REV")
        else:
            self.send_data_signal.emit("TBAS:EVENT:REM")

    def on_alarm_clear(self):
        if "FORC" == self.alarm_mode:
            if self.alarm:
                self.send_data_signal.emit("SYST:ALAR:FORC 0")
            else:
                self.send_data_signal.emit("SYST:ALAR:FORC 1")
        else:
            self.send_data_signal.emit("SYST:ALAR:CLE")

    def on_restart_survey(self):
        self.send_data_signal.emit("GPS:POS:SURV:STAR")
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Sending command")
        msg_box.setText("Requesting survey restart...   ")
        msg_box.setStandardButtons(QMessageBox.Ok)
        QTimer.singleShot(1500, msg_box.close)
        msg_box.exec()

    def update_postion(self, data):
        latitude, longitude, altitude = data.position
        str_direction = " N"
        if latitude < 0.0:
            latitude = -latitude
            str_direction = " S"
        str_latitude = "%0.6f" % latitude
        str_latitude += str_direction
        str_direction = " E"
        if longitude < 0.0:
            longitude = -longitude
            str_direction = " W"
        str_longitude = "%0.6f" % longitude
        str_longitude += str_direction
        str_altitude = "%0.2f m" % altitude
        self.latitude_label.setText(str_latitude)
        self.longitude_label.setText(str_longitude)
        self.altitude_label.setText(str_altitude)
        self.survey_progress.setValue(data.survey)

    def update_satellites(self, data):
        if self.isOldFS740():
            self.legend_gps.hide()
            self.legend_glonass.hide()
            self.legend_beidou.hide()
            self.legend_galileo.hide()
        else:
            self.legend_gps.show()
            self.legend_glonass.show()
            self.legend_beidou.show()
            self.legend_galileo.show()
        self.tracking_label.setText("%d" % len(data.satellites))
        if self.isOldFS740():
            snr = self.compute_snr(data)
        else:
            snr = data.snr
        self.snr_label.setText("%d" % snr)
        self.satellites_widget.set_satellites(data.satellites, data.satellite_info)

    def compute_snr(self, data):
        snr = 0
        snr_data = [sat.snr for sat in data.satellite_info if sat.sv_number in data.satellites]
        snr_data.sort(reverse=True)
        largest_snr = snr_data[0:4]
        if len(largest_snr):
            total = sum(largest_snr)
            snr = total // len(largest_snr)
        return snr

    def update_utc(self, data):
        # Show timing alignment
        if "GPS" == data.time_alignment:
            align_label = "GPS"
        elif "GLON" == data.time_alignment:
            align_label = "GLONASS"
        elif "BEID" == data.time_alignment:
            align_label = "BEIDOU"
        elif "GAL" == data.time_alignment:
            align_label = "GALILEO"
        else:
            align_label = "UTC"
        if 0 != data.local_time_offset:
            align_label = "LOCAL TIME (%s)" % align_label
        self.gbUTC.setTitle(align_label)
        # Show time
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December", "Invalid"]
        if not (1 <= data.time[1] <= 12):
            data.time[1] = 13
        self.labelUTC.setText("%s %d, %04d  /  %02d:%02d:%02.0f" % (months[data.time[1]-1], data.time[2], data.time[0],
                                                             data.time[3], data.time[4], math.floor(data.time[5])))

    def update_gps_status(self, data):
        status = data.gps_status
        self.notime_led.set_led(True if status & 0x01 else False)
        self.antopen_led.set_led(True if status & 0x02 else False)
        self.antshort_led.set_led(True if status & 0x04 else False)
        self.nosat_led.set_led(True if status & 0x08 else False)
        self.utc_led.set_led(True if status & 0x10 else False)
        self.survey_led.set_led(True if status & 0x20 else False)
        self.leapsec_led.set_led(True if status & 0x80 else False)

    def update_timebase(self, data):
        status = data.ques_status
        self.locked_led.set_led(False if status & 0x0004 else True)
        self.stable_led.set_led(False if status & 0x0020 else True)
        self.holdover_led.set_led(True if
                                  data.timebase_state == "MAN" or
                                  data.timebase_state == "NGPS" or
                                  data.timebase_state == "BGPS" else False)
        text = self.timebase_state_desc[data.timebase_state] \
            if data.timebase_state in self.timebase_state_desc else "Unknown"
        self.pllstatus_label.setText(text)
        if data.timebase_state == "LOCK":
            duration = data.lock_duration
        elif data.timebase_state == "POW":
            duration = data.warmup_duration
        else:
            duration = data.holdover_duration
        text = DurationDisplay(duration).get()
        self.duration_label.setText(text)
        text = "%d s" % data.loop_tc
        self.looptc_label.setText(text)
        text = AbbrevTimeDisplay(data.time_err).get()
        if not ("LOCK" == data.timebase_state or "MAN" == data.timebase_state or
                "NGPS" == data.timebase_state or "BGPS" == data.timebase_state):
            text = "--"
        self.timeerr_label.setText(text)
        text = AbbrevTimeDisplay(data.average_err).get()
        if not ("LOCK" == data.timebase_state):
            text = "--"
        self.aveerr_label.setText(text)
        text = "%0.6f V" % data.freq_control
        self.freqcontrol_label.setText(text)

    def update_events(self, data):
        text = "%u" % data.event_count
        self.event_count_label.setText(text)
        text_event = "Unknown"
        text_date = ""
        text_time = ""
        if data.event[0] in self.timebase_state_desc:
            text_event = self.timebase_state_desc[data.event[0]]
            if data.event[0] != "NON":
                text_date = "%u/%u/%04u" % (data.event[2], data.event[3], data.event[1])
                text_time = "%02u:%02u:%02u" % (data.event[4], data.event[5], data.event[6])
        self.event_desc_label.setText(text_event)
        self.event_date_label.setText(text_date)
        self.event_time_label.setText(text_time)

    def update_alarm(self, data):
        if data.alarm:
            self.alarm_status_label.setText("ASSERTED")
            self.alarm_status_label.setStyleSheet("QLabel { color : orange; font-weight : bold }")
        else:
            self.alarm_status_label.setText("Inactive")
            self.alarm_status_label.setStyleSheet("QLabel { }")
        condition_strings = ["Time not from GPS", "In holdover", "Offset from UTC"]
        cause_labels = [self.alarm_cause1_label, self.alarm_cause2_label, self.alarm_cause3_label]
        count = 0
        if data.alarm:
            if "FORC" == data.alarm_mode:
                cause_labels[count].setText("Manually forced")
                count += 1
            else:
                cause = 0
                mask = 1
                condition = data.alarm_condition if "TRAC" == data.alarm_mode else data.alarm_event
                while cause < len(condition_strings):
                    if mask & condition:
                        if count < len(cause_labels):
                            cause_labels[count].setText(condition_strings[cause])
                        count += 1
                    mask <<= 1
                    cause += 1
        else:
            cause_labels[count].setText("None")
            count += 1
        if not count:
            cause_labels[count].setText("Unknown")
            count += 1
        while count < len(cause_labels):
            cause_labels[count].setText("")
            count += 1
        if "TRAC" == data.alarm_mode:
            self.alarm_clear_btn.hide()
        else:
            self.alarm_clear_btn.show()
            text = "Assert" if "FORC" == data.alarm_mode and not data.alarm else "Clear"
            self.alarm_clear_btn.setText(text)
            enabled = False if "LATC" == data.alarm_mode and not data.alarm else True
            self.alarm_clear_btn.setEnabled(enabled)
        # Remember state so we can respond to button correctly
        self.alarm_mode = data.alarm_mode
        self.alarm = data.alarm
