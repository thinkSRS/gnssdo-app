# Copyright: Stanford Reserach Systems, Inc and contributors
# License: GNU GPL, version 3 or later; https://www.gnu.org/licenses/gpl-3.0.html
"""Gps setup form for configuring gpsdo"""
import math

from PyQt5.QtCore import (pyqtSignal)
from PyQt5.QtWidgets import (QWidget, QDialog, QFormLayout, QVBoxLayout, QHBoxLayout,
                             QLabel, QComboBox, QCheckBox, QSpinBox, QDoubleSpinBox,
                             QDialogButtonBox, QMessageBox)

from ui import gpssetup_ui
from data_display import (AbbrevTimeDisplay, TimeDelayDisplay)


class TimebaseData:
    def __init__(self, rhs):
        self.lock_gnss = rhs.lock_gnss
        self.bandwidth = rhs.bandwidth
        self.manual_time_constant = rhs.manual_time_constant
        self.holdover_mode = rhs.holdover_mode
        self.holdover_limit = rhs.holdover_limit


class GpsConfigData:
    def __init__(self, rhs):
        self.constellation = rhs.constellation
        self.time_alignment = rhs.time_alignment
        self.time_quality = rhs.time_quality
        self.min_snr = rhs.min_snr
        self.min_elevation = rhs.min_elevation
        self.local_time_offset = rhs.local_time_offset
        self.survey_mode = rhs.survey_mode
        self.survey_fixes = rhs.survey_fixes
        self.antenna_delay = rhs.antenna_delay


class AlarmConfigData:
    def __init__(self, rhs):
        self.alarm_mode = rhs.alarm_mode
        self.alarm_holdover_duration = rhs.alarm_holdover_duration
        self.alarm_offset_limit = rhs.alarm_offset_limit
        self.alarm_enable = rhs.alarm_enable


class PulseConfigData:
    def __init__(self, rhs):
        self.pulse_offset = rhs.pulse_offset


class GpsSetupWidget(QWidget, gpssetup_ui.Ui_Form):
    send_data_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        # Call Qt Designer setup code
        self.setupUi(self)
        self.setup_data = None
        self.model = "FS752"
        self.version = 0.50
        self.edit_timebase_btn.clicked.connect(self.on_edit_timebase)
        self.edit_receiver_btn.clicked.connect(self.on_edit_receiver)
        self.edit_alarm_btn.clicked.connect(self.on_edit_alarm)
        self.edit_1pps_btn.clicked.connect(self.on_edit_1pps)

    def is_old_fs740(self):
        return "FS740" == self.model and self.version < 4.00

    def on_edit_timebase(self):
        dlg = TimebaseConfigDlg(self, self.setup_data)
        dlg.setWindowTitle("Configure Timebase Settings")
        dlg.setMinimumWidth(300)
        dlg.setModal(True)
        if dlg.exec():
            # Update timebase config
            cmd = "TBAS:CONF:LOCK %d" % dlg.timebase_data.lock_gnss
            self.send_data_signal.emit(cmd)
            cmd = "TBAS:CONF:BWID %s" % dlg.timebase_data.bandwidth
            self.send_data_signal.emit(cmd)
            cmd = "TBAS:TCON %d" % dlg.timebase_data.manual_time_constant
            self.send_data_signal.emit(cmd)
            cmd = "TBAS:CONF:HMOD %s" % dlg.timebase_data.holdover_mode
            self.send_data_signal.emit(cmd)
            cmd = "TBAS:CONF:LIM %0.12e" % dlg.timebase_data.holdover_limit
            self.send_data_signal.emit(cmd)

    def on_edit_receiver(self):
        dlg = GpsConfigDlg(self, self.setup_data, self.model, self.version)
        dlg.setWindowTitle("Configure GNSS Receiver")
        dlg.setMinimumWidth(300)
        dlg.setModal(True)
        if dlg.exec():
            # Update receiver config
            if not self.is_old_fs740():
                cmd = "GPS:CONF:CONS %d" % dlg.gps_config_data.constellation
                self.send_data_signal.emit(cmd)
            cmd = "GPS:CONF:ALIG %s" % dlg.gps_config_data.time_alignment
            self.send_data_signal.emit(cmd)
            cmd = "GPS:CONF:QUAL %s" % dlg.gps_config_data.time_quality
            self.send_data_signal.emit(cmd)
            cmd = "GPS:CONF:MODE 1,%0.8e,%0.0f" % (dlg.gps_config_data.min_elevation * math.pi / 180.0, dlg.gps_config_data.min_snr)
            self.send_data_signal.emit(cmd)
            cmd = "GPS:CONF:SURV %s" % dlg.gps_config_data.survey_mode
            self.send_data_signal.emit(cmd)
            cmd = "GPS:CONF:SURV:FIX %u" % dlg.gps_config_data.survey_fixes
            self.send_data_signal.emit(cmd)
            cmd = "GPS:CONF:ADEL %0.12f" % dlg.gps_config_data.antenna_delay
            self.send_data_signal.emit(cmd)
            cmd = "SYST:TIM:LOFF %0.12f" % dlg.gps_config_data.local_time_offset
            self.send_data_signal.emit(cmd)
            cmd = "GPS:CONF:SAV"
            self.send_data_signal.emit(cmd)

    def on_edit_alarm(self):
        dlg = AlarmConfigDlg(self, self.setup_data)
        dlg.setWindowTitle("Alarm Configuration")
        dlg.setMinimumWidth(300)
        dlg.setModal(True)
        if dlg.exec():
            # Update alarm config
            cmd = "SYST:ALAR:MOD %s" % dlg.alarm_config_data.alarm_mode
            self.send_data_signal.emit(cmd)
            cmd = "SYST:ALAR:ENAB %d" % dlg.alarm_config_data.alarm_enable
            self.send_data_signal.emit(cmd)
            cmd = "SYST:ALAR:DUR %d" % dlg.alarm_config_data.alarm_holdover_duration
            self.send_data_signal.emit(cmd)
            cmd = "SYST:ALAR:TINT %0.9f" % dlg.alarm_config_data.alarm_offset_limit
            self.send_data_signal.emit(cmd)

    def on_edit_1pps(self):
        dlg = PulseConfigDlg(self, self.setup_data)
        dlg.setWindowTitle("Pulse Configuration")
        dlg.setMinimumWidth(300)
        dlg.setModal(True)
        if dlg.exec():
            # Update pulse config
            if "FS740" == self.model:
                cmd_str = "SOUR3:PHAS:SYNC:TDEL"
            else:
                cmd_str = "SOUR:PHAS:SYNC:TDEL"
            cmd = "%s %0.12e" % (cmd_str, dlg.pulse_config_data.pulse_offset)
            self.send_data_signal.emit(cmd)

    def on_gps_setup(self, setup):
        self.setup_data = setup
        self.serial = setup.serial
        self.model = setup.model
        self.version = float(setup.version[0:4])
        self.update_timebase_setup()
        self.update_gps_setup()
        self.update_alarm_setup()
        self.update_pulse_setup()
        self.update_device_info()

    def update_timebase_setup(self):
        setup = self.setup_data
        self.lock_to_gps_label.setText("Yes" if setup.lock_gnss else "No")
        self.loop_bandwidth_label.setText("Manual" if "MAN" == setup.bandwidth else "Automatic")
        self.manual_time_constant_label.setText("%u s" % setup.manual_time_constant)
        abbrev_time = AbbrevTimeDisplay(setup.holdover_limit)
        self.holdover_error_label.setText(abbrev_time.get())
        text = "Jump to good 1pps"
        if "WAIT" == setup.holdover_mode:
            text = "Wait for good 1pps"
        elif "SLEW" == setup.holdover_mode:
            text = "Slew to good 1pps"
        self.leave_holdover_label.setText(text)

    def update_gps_setup(self):
        setup = self.setup_data
        if self.is_old_fs740():
            self.constellations_caption.hide()
            self.track_gps_checkbox.hide()
            self.track_glonass_checkbox.hide()
            self.track_beidou_checkbox.hide()
            self.track_galileo_checkbox.hide()
        else:
            self.track_gps_checkbox.setChecked(True if (setup.constellation & 1) else False)
            self.track_glonass_checkbox.setChecked(True if (setup.constellation & 2) else False)
            self.track_beidou_checkbox.setChecked(True if (setup.constellation & 4) else False)
            self.track_galileo_checkbox.setChecked(True if (setup.constellation & 8) else False)
            self.constellations_caption.show()
            self.track_gps_checkbox.show()
            self.track_glonass_checkbox.show()
            self.track_beidou_checkbox.show()
            self.track_galileo_checkbox.show()
        text = "Align to "
        if "UTC" == setup.time_alignment:
            text += "UTC"
        elif "GPS" == setup.time_alignment:
            text += "GPS"
        elif "GLON" == setup.time_alignment:
            text += "GLONASS"
        elif "BEID" == setup.time_alignment:
            text += "BEIDOU"
        elif "GAL" == setup.time_alignment:
            text += "GALILEO"
        else:
            text += "UNKNOWN"
        self.timing_alignment_label.setText(text)
        self.timing_quality_label.setText("Require only 1 satellite" if setup.time_quality == "1SAT" else "Require 3 satellites")
        self.min_snr_label.setText("%0.0f" % setup.min_snr)
        self.min_sat_elevation_label.setText("%0.0f Deg" % setup.min_elevation)
        self.local_time_offset_label.setText("%0.1f hr" % (setup.local_time_offset/3600.0))
        if "DIS" == setup.survey_mode:
            text = "Disabled"
        elif "RED" == setup.survey_mode:
            text = "Redo survey at power on"
        elif "REM" == setup.survey_mode:
            text = "Remember survey results"
        else:
            text = "Unknown mode"
        self.position_survey_label.setText(text)
        self.position_fixes_label.setText("%u" % setup.survey_fixes)
        delay_time = TimeDelayDisplay(setup.antenna_delay, digits=0)
        self.antenna_correction_label.setText(delay_time.get())

    def update_alarm_setup(self):
        setup = self.setup_data
        if "FORC" == setup.alarm_mode:
            text = "Manually set state"
        elif "TRAC" == setup.alarm_mode:
            text = "Track current condition"
        elif "LATC" == setup.alarm_mode:
            text = "Latch alarm condition"
        else:
            text = "Unknown"
        self.alarm_mode_label.setText(text)
        text = "In holdover for more than %d s" % setup.alarm_holdover_duration
        self.in_holdver_checkbox.setText(text)
        offset_display = AbbrevTimeDisplay(setup.alarm_offset_limit, 0)
        text = "Offset from UTC more than %s" % offset_display.get()
        self.offset_from_utc_checkbox.setText(text)
        self.not_from_gps_checkbox.setChecked(True if (setup.alarm_enable & 1) else False)
        self.in_holdver_checkbox.setChecked(True if (setup.alarm_enable & 2) else False)
        self.offset_from_utc_checkbox.setChecked(True if (setup.alarm_enable & 4) else False)

    def update_pulse_setup(self):
        setup = self.setup_data
        offset = setup.pulse_offset
        pulse_display = TimeDelayDisplay(offset, digits=3).get()
        self.time_offset_label.setText(pulse_display)

    def update_device_info(self):
        setup = self.setup_data
        self.model_label.setText(setup.model)
        self.serial_number_label.setText(setup.serial)
        self.firmware_version_label.setText(setup.version)
        self.gnss_receiver_label.setText(setup.gps_model)
        self.receiver_version_label.setText(setup.gps_version)
        self.options_label.setText("".join([str(opt) for opt in setup.options]))


class TimebaseConfigDlg(QDialog):
    def __init__(self, parent, timebase_data):
        super().__init__(parent)
        self.timebase_data = TimebaseData(timebase_data)
        # Layout form
        dlg_layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        caption_lock = QLabel(self)
        caption_lock.setText("Lock to GNSS:")
        self.lock_combobox = QComboBox(self)
        self.lock_combobox.addItem("Yes")
        self.lock_combobox.addItem("No")
        form_layout.setWidget(0, QFormLayout.LabelRole, caption_lock)
        form_layout.setWidget(0, QFormLayout.FieldRole, self.lock_combobox)
        caption_bandwidth = QLabel(self)
        caption_bandwidth.setText("Loop Bandwidth Control:")
        self.bandwidth_combobox = QComboBox(self)
        self.bandwidth_combobox.addItem("Automatic")
        self.bandwidth_combobox.addItem("Manual")
        form_layout.setWidget(1, QFormLayout.LabelRole, caption_bandwidth)
        form_layout.setWidget(1, QFormLayout.FieldRole, self.bandwidth_combobox)
        caption_manual_tc = QLabel(self)
        caption_manual_tc.setText("Manual Time Consant:")
        self.manual_tc_spinbox = QSpinBox(self)
        self.manual_tc_spinbox.setMinimum(3)
        self.manual_tc_spinbox.setMaximum(1000000)
        form_layout.setWidget(2, QFormLayout.LabelRole, caption_manual_tc)
        form_layout.setWidget(2, QFormLayout.FieldRole, self.manual_tc_spinbox)
        caption_holdover_error = QLabel(self)
        caption_holdover_error.setText("Enter Holdover if Error (us) >")
        self.holdover_error_spinbox = QDoubleSpinBox(self)
        self.holdover_error_spinbox.setMinimum(0.1)
        self.holdover_error_spinbox.setMaximum(1000000.0)
        self.holdover_error_spinbox.setDecimals(3)
        form_layout.setWidget(3, QFormLayout.LabelRole, caption_holdover_error)
        form_layout.setWidget(3, QFormLayout.FieldRole, self.holdover_error_spinbox)
        caption_holdover_mode = QLabel(self)
        caption_holdover_mode.setText("To Leave Holdover:")
        self.holdover_mode_combobox = QComboBox(self)
        self.holdover_mode_combobox.addItem("Wait for Good 1pps")
        self.holdover_mode_combobox.addItem("Jump to Good 1pps")
        self.holdover_mode_combobox.addItem("Slew to Good 1pps")
        form_layout.setWidget(4, QFormLayout.LabelRole, caption_holdover_mode)
        form_layout.setWidget(4, QFormLayout.FieldRole, self.holdover_mode_combobox)
        dlg_layout.addLayout(form_layout)
        # Layout dialog buttons
        dialog_btns = QDialogButtonBox(self)
        dialog_btns.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        dlg_layout.addWidget(dialog_btns)
        # Initialize widgets
        self.lock_combobox.setCurrentIndex(0 if timebase_data.lock_gnss else 1)
        self.bandwidth_combobox.setCurrentIndex((0 if "AUT" == timebase_data.bandwidth else 1))
        self.manual_tc_spinbox.setValue(timebase_data.manual_time_constant)
        self.holdover_error_spinbox.setValue(timebase_data.holdover_limit*1e6)
        mode = 1
        if "WAIT" == timebase_data.holdover_mode:
            mode = 0
        elif "SLEW" == timebase_data.holdover_mode:
            mode = 2
        self.holdover_mode_combobox.setCurrentIndex(mode)
        # Connect signals
        dialog_btns.accepted.connect(self.on_ok)
        dialog_btns.rejected.connect(self.reject)

    def on_ok(self):
        self.timebase_data.lock_gnss = 1 if 0 == self.lock_combobox.currentIndex() else 0
        self.timebase_data.bandwidth = "AUT" if 0 == self.bandwidth_combobox.currentIndex() else "MAN"
        self.timebase_data.manual_time_constant = self.manual_tc_spinbox.value()
        self.timebase_data.holdover_limit = self.holdover_error_spinbox.value()/1e6
        mode = "JUMP"
        if 0 == self.holdover_mode_combobox.currentIndex():
            mode = "WAIT"
        elif 2 == self.holdover_mode_combobox.currentIndex():
            mode = "SLEW"
        self.timebase_data.holdover_mode = mode
        self.accept()


class GpsConfigDlg(QDialog):
    def __init__(self, parent, gps_config_data, model, version):
        super().__init__(parent)
        self.gps_config_data = GpsConfigData(gps_config_data)
        self.model = model
        self.version = version
        # Layout form
        dlg_layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        caption_constellation = QLabel(self)
        caption_constellation.setText("Constellations Tracked:\n\n  (Not all combos supported)")
        gnss_layout = QVBoxLayout()
        self.gps_checkbox = QCheckBox(self)
        self.gps_checkbox.setText("GPS")
        self.glonass_checkbox = QCheckBox(self)
        self.glonass_checkbox.setText("GLONASS")
        self.beidou_checkbox = QCheckBox(self)
        self.beidou_checkbox.setText("BEIDOU")
        self.galileo_checkbox = QCheckBox(self)
        self.galileo_checkbox.setText("GALILEO")
        gnss_layout.addWidget(self.gps_checkbox)
        gnss_layout.addWidget(self.glonass_checkbox)
        gnss_layout.addWidget(self.beidou_checkbox)
        gnss_layout.addWidget(self.galileo_checkbox)
        if self.is_old_fs740():
            caption_constellation.hide()
            self.gps_checkbox.hide()
            self.glonass_checkbox.hide()
            self.beidou_checkbox.hide()
            self.galileo_checkbox.hide()
        form_layout.setWidget(0, QFormLayout.LabelRole, caption_constellation)
        form_layout.setLayout(0, QFormLayout.FieldRole, gnss_layout)
        caption_alignment = QLabel(self)
        caption_alignment.setText("Timing Alignment:")
        self.align_combobox = QComboBox(self)
        self.align_combobox.addItem("Align to UTC")
        self.align_combobox.addItem("Align to GPS")
        if not self.is_old_fs740():
            self.align_combobox.addItem("Align to GLONASS")
            self.align_combobox.addItem("Align to BEIDOU")
            self.align_combobox.addItem("Align to GALILEO")
        form_layout.setWidget(1, QFormLayout.LabelRole, caption_alignment)
        form_layout.setWidget(1, QFormLayout.FieldRole, self.align_combobox)
        caption_quality = QLabel(self)
        caption_quality.setText("Timing Quality:")
        self.quality_combobox = QComboBox(self)
        self.quality_combobox.addItem("Require only 1 satellite")
        self.quality_combobox.addItem("Require 3 satellites")
        form_layout.setWidget(2, QFormLayout.LabelRole, caption_quality)
        form_layout.setWidget(2, QFormLayout.FieldRole, self.quality_combobox)
        caption_min_snr = QLabel(self)
        caption_min_snr.setText("Minimum SNR:")
        self.min_snr_spinbox = QSpinBox(self)
        self.min_snr_spinbox.setMinimum(0)
        self.min_snr_spinbox.setMaximum(55)
        form_layout.setWidget(3, QFormLayout.LabelRole, caption_min_snr)
        form_layout.setWidget(3, QFormLayout.FieldRole, self.min_snr_spinbox)
        caption_min_elevation = QLabel(self)
        caption_min_elevation.setText("Minimum Sat. Elevation (Deg):")
        self.min_elevation_spinbox = QSpinBox(self)
        self.min_elevation_spinbox.setMinimum(0)
        self.min_elevation_spinbox.setMaximum(90)
        form_layout.setWidget(4, QFormLayout.LabelRole, caption_min_elevation)
        form_layout.setWidget(4, QFormLayout.FieldRole, self.min_elevation_spinbox)
        caption_survey_mode = QLabel(self)
        caption_survey_mode.setText("Position Survey:")
        self.survey_combobox = QComboBox(self)
        self.survey_combobox.addItem("Disabled")
        self.survey_combobox.addItem("Redo survey at power on")
        self.survey_combobox.addItem("Remember survey results")
        form_layout.setWidget(5, QFormLayout.LabelRole, caption_survey_mode)
        form_layout.setWidget(5, QFormLayout.FieldRole, self.survey_combobox)
        caption_survey_fixes = QLabel(self)
        caption_survey_fixes.setText("Position Fixes in Survey:")
        self.fixes_spinbox = QSpinBox(self)
        self.fixes_spinbox.setMinimum(1)
        self.fixes_spinbox.setMaximum(2**31 - 1)
        form_layout.setWidget(6, QFormLayout.LabelRole, caption_survey_fixes)
        form_layout.setWidget(6, QFormLayout.FieldRole, self.fixes_spinbox)
        caption_antenna_delay = QLabel(self)
        caption_antenna_delay.setText("Antenna Delay Correction (ns):")
        self.antenna_delay_spinbox = QSpinBox(self)
        self.antenna_delay_spinbox.setMinimum(-32768)
        self.antenna_delay_spinbox.setMaximum(32767)
        form_layout.setWidget(7, QFormLayout.LabelRole, caption_antenna_delay)
        form_layout.setWidget(7, QFormLayout.FieldRole, self.antenna_delay_spinbox)
        caption_local_time_offset = QLabel(self)
        caption_local_time_offset.setText("Local Time Offset (hr):")
        self.local_offset_spinbox = QDoubleSpinBox(self)
        self.local_offset_spinbox.setDecimals(1)
        self.local_offset_spinbox.setMinimum(-24.0)
        self.local_offset_spinbox.setMaximum(+24.0)
        form_layout.setWidget(8, QFormLayout.LabelRole, caption_local_time_offset)
        form_layout.setWidget(8, QFormLayout.FieldRole, self.local_offset_spinbox)
        dlg_layout.addLayout(form_layout)
        # Layout dialog buttons
        dialog_btns = QDialogButtonBox(self)
        dialog_btns.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        dlg_layout.addWidget(dialog_btns)
        # Initialize widgets
        if not self.is_old_fs740():
            self.gps_checkbox.setChecked(True if (gps_config_data.constellation & 1) else False)
            self.glonass_checkbox.setChecked(True if (gps_config_data.constellation & 2) else False)
            self.beidou_checkbox.setChecked(True if (gps_config_data.constellation & 4) else False)
            self.galileo_checkbox.setChecked(True if (gps_config_data.constellation & 8) else False)
        if self.is_old_fs740():
            if "GPS" == gps_config_data.time_alignment:
                index = 1
            else:
                index = 0
        else:
            if "GPS" == gps_config_data.time_alignment:
                index = 1
            elif "GLON" == gps_config_data.time_alignment:
                index = 2
            elif "BEID" == gps_config_data.time_alignment:
                index = 3
            elif "GAL" == gps_config_data.time_alignment:
                index = 4
            else:
                index = 0
        self.align_combobox.setCurrentIndex(index)
        self.quality_combobox.setCurrentIndex(0 if "1SAT" == gps_config_data.time_quality else 1)
        if "DIS" == gps_config_data.survey_mode:
            index = 0
        elif "REM" == gps_config_data.survey_mode:
            index = 2
        else:
            index = 1
        self.survey_combobox.setCurrentIndex(index)
        self.min_snr_spinbox.setValue(round(gps_config_data.min_snr))
        self.min_elevation_spinbox.setValue(round(gps_config_data.min_elevation))
        self.fixes_spinbox.setValue(gps_config_data.survey_fixes)
        self.antenna_delay_spinbox.setValue(int(round(gps_config_data.antenna_delay*1e9)))
        self.local_offset_spinbox.setValue(gps_config_data.local_time_offset/3600.0)
        # Connect signals
        dialog_btns.accepted.connect(self.on_ok)
        dialog_btns.rejected.connect(self.reject)

    def is_old_fs740(self):
        return "FS740" == self.model and self.version < 4.00

    def on_ok(self):
        if self.is_old_fs740():
            constellation = 1
        else:
            constellation = 0
            if self.gps_checkbox.isChecked():
                constellation |= 1
            if self.glonass_checkbox.isChecked():
                constellation |= 2
            if self.beidou_checkbox.isChecked():
                constellation |= 4
            if self.galileo_checkbox.isChecked():
                constellation |= 8
        self.gps_config_data.constellation = constellation
        index = self.align_combobox.currentIndex()
        if 1 == index:
            self.gps_config_data.time_alignment = "GPS"
        elif 2 == index:
            self.gps_config_data.time_alignment = "GLON"
        elif 3 == index:
            self.gps_config_data.time_alignment = "BEID"
        elif 4 == index:
            self.gps_config_data.time_alignment = "GAL"
        else:
            self.gps_config_data.time_alignment = "UTC"
        self.gps_config_data.time_quality = "1SAT" if 0 == self.quality_combobox.currentIndex() else "3SAT"
        self.gps_config_data.min_snr = self.min_snr_spinbox.value()
        self.gps_config_data.min_elevation = self.min_elevation_spinbox.value()
        index = self.survey_combobox.currentIndex()
        if 0 == index:
            self.gps_config_data.survey_mode = "DIS"
        elif 2 == index:
            self.gps_config_data.survey_mode = "REM"
        else:
            self.gps_config_data.survey_mode = "RED"
        self.gps_config_data.survey_fixes = self.fixes_spinbox.value()
        self.gps_config_data.antenna_delay = self.antenna_delay_spinbox.value()/1e9
        self.gps_config_data.local_time_offset = int(round(self.local_offset_spinbox.value()*3600))
        # Timing alignment must include a followed constellation
        if 0 == constellation:
            QMessageBox.critical(self, "Error", "Must track at least one GNSS constellation")
        elif "UTC" == self.gps_config_data.time_alignment or \
                ("GPS" == self.gps_config_data.time_alignment and (self.gps_config_data.constellation & 1)) or \
                ("GLON" == self.gps_config_data.time_alignment and (self.gps_config_data.constellation & 2)) or \
                ("BEID" == self.gps_config_data.time_alignment and (self.gps_config_data.constellation & 4)) or \
                ("GAL" == self.gps_config_data.time_alignment and (self.gps_config_data.constellation & 8)):
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Timing alignment must include a tracked constellation")


class AlarmConfigDlg(QDialog):
    def __init__(self, parent, alarm_config_data):
        super().__init__(parent)
        self.alarm_config_data = AlarmConfigData(alarm_config_data)
        # Layout form
        dlg_layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        caption_mode = QLabel(self)
        caption_mode.setText("Alarm Mode:")
        self.mode_combobox = QComboBox(self)
        self.mode_combobox.addItem("Track current condition")
        self.mode_combobox.addItem("Latch alarm condition")
        self.mode_combobox.addItem("Manually set state")
        form_layout.setWidget(0, QFormLayout.LabelRole, caption_mode)
        form_layout.setWidget(0, QFormLayout.FieldRole, self.mode_combobox)
        dlg_layout.addLayout(form_layout)
        dlg_layout.addSpacing(5)
        # Assert layout
        assert_layout = QFormLayout()
        caption_assert = QLabel(self)
        caption_assert.setText("Assert Condition:")
        caption_limit = QLabel(self)
        caption_limit.setText("Limit:")
        assert_layout.setWidget(0, QFormLayout.LabelRole, caption_assert)
        assert_layout.setWidget(0, QFormLayout.FieldRole, caption_limit)
        self.not_from_gps_checkbox = QCheckBox()
        self.not_from_gps_checkbox.setText("Time not from GPS")
        self.in_holdover_checkbox = QCheckBox()
        self.in_holdover_checkbox.setText("In holdover for more than (s)")
        self.offset_from_utc_checkbox = QCheckBox()
        self.offset_from_utc_checkbox.setText("Offset from UTC more than (ns)")
        self.holdover_duration_spinbox = QSpinBox()
        self.holdover_duration_spinbox.setMinimum(0)
        self.holdover_duration_spinbox.setMaximum(2**31 - 1)
        self.offset_from_utc_spinbox = QSpinBox()
        self.offset_from_utc_spinbox.setMinimum(50)
        self.offset_from_utc_spinbox.setMaximum(1000000000)
        offset_spacing = 20
        not_from_gps_layout = QHBoxLayout()
        not_from_gps_layout.addSpacing(offset_spacing)
        not_from_gps_layout.addWidget(self.not_from_gps_checkbox)
        assert_layout.setLayout(1, QFormLayout.LabelRole, not_from_gps_layout)
        in_holdover_layout = QHBoxLayout()
        in_holdover_layout.addSpacing(offset_spacing)
        in_holdover_layout.addWidget(self.in_holdover_checkbox)
        assert_layout.setLayout(2, QFormLayout.LabelRole, in_holdover_layout)
        assert_layout.setWidget(2, QFormLayout.FieldRole, self.holdover_duration_spinbox)
        offset_from_utc_layout = QHBoxLayout()
        offset_from_utc_layout.addSpacing(offset_spacing)
        offset_from_utc_layout.addWidget(self.offset_from_utc_checkbox)
        assert_layout.setLayout(3, QFormLayout.LabelRole, offset_from_utc_layout)
        assert_layout.setWidget(3, QFormLayout.FieldRole, self.offset_from_utc_spinbox)
        dlg_layout.addLayout(assert_layout)
        dlg_layout.addStretch(1)
        # Layout dialog buttons
        dialog_btns = QDialogButtonBox(self)
        dialog_btns.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        dlg_layout.addWidget(dialog_btns)
        # Initialize widgets
        if "FORC" == alarm_config_data.alarm_mode:
            index = 2
        elif "LATC" == alarm_config_data.alarm_mode:
            index = 1
        else:
            index = 0
        self.mode_combobox.setCurrentIndex(index)
        self.not_from_gps_checkbox.setChecked(True if (alarm_config_data.alarm_enable & 1) else False)
        self.in_holdover_checkbox.setChecked(True if (alarm_config_data.alarm_enable & 2) else False)
        self.offset_from_utc_checkbox.setChecked(True if (alarm_config_data.alarm_enable & 4) else False)
        self.holdover_duration_spinbox.setValue(alarm_config_data.alarm_holdover_duration)
        self.offset_from_utc_spinbox.setValue(int(alarm_config_data.alarm_offset_limit*1e9))
        # Connect signals
        dialog_btns.accepted.connect(self.on_ok)
        dialog_btns.rejected.connect(self.reject)

    def on_ok(self):
        index = self.mode_combobox.currentIndex()
        if 2 == index:
            self.alarm_config_data.alarm_mode = "FORC"
        elif 1 == index:
            self.alarm_config_data.alarm_mode = "LATC"
        else:
            self.alarm_config_data.alarm_mode = "TRAC"
        self.alarm_config_data.alarm_enable = 0
        if self.not_from_gps_checkbox.isChecked():
            self.alarm_config_data.alarm_enable |= 1
        if self.in_holdover_checkbox.isChecked():
            self.alarm_config_data.alarm_enable |= 2
        if self.offset_from_utc_checkbox.isChecked():
            self.alarm_config_data.alarm_enable |= 4
        self.alarm_config_data.alarm_holdover_duration = self.holdover_duration_spinbox.value()
        self.alarm_config_data.alarm_offset_limit = self.offset_from_utc_spinbox.value()/1e9
        self.accept()


class PulseConfigDlg(QDialog):
    def __init__(self, parent, pulse_config_data):
        super().__init__(parent)
        self.setObjectName("pulse_config_dlg")
        self.pulse_config_data = PulseConfigData(pulse_config_data)
        # Layout form
        dlg_layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        caption_offset = QLabel(self)
        caption_offset.setText("Time Offset (ns):")
        self.offset_spinbox = QDoubleSpinBox(self)
        self.offset_spinbox.setMinimum(-1000000000.0)
        self.offset_spinbox.setMaximum(+1000000000.0)
        self.offset_spinbox.setDecimals(3)
        form_layout.setWidget(0, QFormLayout.LabelRole, caption_offset)
        form_layout.setWidget(0, QFormLayout.FieldRole, self.offset_spinbox)
        dlg_layout.addLayout(form_layout)
        # Layout dialog buttons
        dialog_btns = QDialogButtonBox(self)
        dialog_btns.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        dlg_layout.addWidget(dialog_btns)
        # Initialize widgets
        self.offset_spinbox.setValue(self.pulse_config_data.pulse_offset*1e9)
        # Connect signals
        dialog_btns.accepted.connect(self.on_ok)
        dialog_btns.rejected.connect(self.reject)

    def on_ok(self):
        self.pulse_config_data.pulse_offset = self.offset_spinbox.value()/1e9
        self.accept()
