# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gpsstatus_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(559, 410)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.gbUTC = QtWidgets.QGroupBox(Form)
        self.gbUTC.setObjectName("gbUTC")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.gbUTC)
        self.verticalLayout_2.setContentsMargins(-1, 4, -1, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.labelUTC = QtWidgets.QLabel(self.gbUTC)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.labelUTC.setFont(font)
        self.labelUTC.setAlignment(QtCore.Qt.AlignCenter)
        self.labelUTC.setObjectName("labelUTC")
        self.verticalLayout_2.addWidget(self.labelUTC)
        self.gridLayout.addWidget(self.gbUTC, 0, 0, 1, 2)
        self.gbWarnings = QtWidgets.QGroupBox(Form)
        self.gbWarnings.setObjectName("gbWarnings")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.gbWarnings)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.notime_led = StatusCheckBox(self.gbWarnings)
        self.notime_led.setCheckable(True)
        self.notime_led.setObjectName("notime_led")
        self.verticalLayout_3.addWidget(self.notime_led)
        self.antopen_led = StatusCheckBox(self.gbWarnings)
        self.antopen_led.setCheckable(True)
        self.antopen_led.setObjectName("antopen_led")
        self.verticalLayout_3.addWidget(self.antopen_led)
        self.antshort_led = StatusCheckBox(self.gbWarnings)
        self.antshort_led.setCheckable(True)
        self.antshort_led.setObjectName("antshort_led")
        self.verticalLayout_3.addWidget(self.antshort_led)
        self.nosat_led = StatusCheckBox(self.gbWarnings)
        self.nosat_led.setCheckable(True)
        self.nosat_led.setObjectName("nosat_led")
        self.verticalLayout_3.addWidget(self.nosat_led)
        self.utc_led = StatusCheckBox(self.gbWarnings)
        self.utc_led.setCheckable(True)
        self.utc_led.setObjectName("utc_led")
        self.verticalLayout_3.addWidget(self.utc_led)
        self.survey_led = StatusCheckBox(self.gbWarnings)
        self.survey_led.setCheckable(True)
        self.survey_led.setObjectName("survey_led")
        self.verticalLayout_3.addWidget(self.survey_led)
        self.leapsec_led = StatusCheckBox(self.gbWarnings)
        self.leapsec_led.setCheckable(True)
        self.leapsec_led.setObjectName("leapsec_led")
        self.verticalLayout_3.addWidget(self.leapsec_led)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.gridLayout.addWidget(self.gbWarnings, 0, 2, 2, 1)
        self.gbPosition = QtWidgets.QGroupBox(Form)
        self.gbPosition.setObjectName("gbPosition")
        self.formLayout_2 = QtWidgets.QFormLayout(self.gbPosition)
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label = QtWidgets.QLabel(self.gbPosition)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.latitude_label = QtWidgets.QLabel(self.gbPosition)
        self.latitude_label.setObjectName("latitude_label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.latitude_label)
        self.label_2 = QtWidgets.QLabel(self.gbPosition)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.longitude_label = QtWidgets.QLabel(self.gbPosition)
        self.longitude_label.setObjectName("longitude_label")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.longitude_label)
        self.label_3 = QtWidgets.QLabel(self.gbPosition)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.altitude_label = QtWidgets.QLabel(self.gbPosition)
        self.altitude_label.setObjectName("altitude_label")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.altitude_label)
        self.label_4 = QtWidgets.QLabel(self.gbPosition)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.survey_progress = QtWidgets.QProgressBar(self.gbPosition)
        self.survey_progress.setProperty("value", 0)
        self.survey_progress.setTextVisible(True)
        self.survey_progress.setObjectName("survey_progress")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.survey_progress)
        self.restart_btn = QtWidgets.QPushButton(self.gbPosition)
        self.restart_btn.setObjectName("restart_btn")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.restart_btn)
        self.gridLayout.addWidget(self.gbPosition, 1, 0, 1, 1)
        self.gbSatellites = QtWidgets.QGroupBox(Form)
        self.gbSatellites.setObjectName("gbSatellites")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.gbSatellites)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_5 = QtWidgets.QLabel(self.gbSatellites)
        self.label_5.setObjectName("label_5")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.tracking_label = QtWidgets.QLabel(self.gbSatellites)
        self.tracking_label.setObjectName("tracking_label")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.tracking_label)
        self.label_6 = QtWidgets.QLabel(self.gbSatellites)
        self.label_6.setObjectName("label_6")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.snr_label = QtWidgets.QLabel(self.gbSatellites)
        self.snr_label.setObjectName("snr_label")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.snr_label)
        self.legend_gps = StatusCheckBox(self.gbSatellites)
        self.legend_gps.setObjectName("legend_gps")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.legend_gps)
        self.legend_glonass = StatusCheckBox(self.gbSatellites)
        self.legend_glonass.setObjectName("legend_glonass")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.legend_glonass)
        self.legend_galileo = StatusCheckBox(self.gbSatellites)
        self.legend_galileo.setObjectName("legend_galileo")
        self.formLayout_3.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.legend_galileo)
        self.legend_beidou = StatusCheckBox(self.gbSatellites)
        self.legend_beidou.setObjectName("legend_beidou")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.legend_beidou)
        self.horizontalLayout_3.addLayout(self.formLayout_3)
        self.satellites_widget = SatellitesWidget(self.gbSatellites)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.satellites_widget.sizePolicy().hasHeightForWidth())
        self.satellites_widget.setSizePolicy(sizePolicy)
        self.satellites_widget.setMinimumSize(QtCore.QSize(75, 75))
        self.satellites_widget.setObjectName("satellites_widget")
        self.horizontalLayout_3.addWidget(self.satellites_widget)
        self.gridLayout.addWidget(self.gbSatellites, 1, 1, 1, 1)
        self.gbTimebase = QtWidgets.QGroupBox(Form)
        self.gbTimebase.setObjectName("gbTimebase")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.gbTimebase)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.locked_led = StatusCheckBox(self.gbTimebase)
        self.locked_led.setObjectName("locked_led")
        self.horizontalLayout_4.addWidget(self.locked_led)
        self.stable_led = StatusCheckBox(self.gbTimebase)
        self.stable_led.setObjectName("stable_led")
        self.horizontalLayout_4.addWidget(self.stable_led)
        self.holdover_led = StatusCheckBox(self.gbTimebase)
        self.holdover_led.setObjectName("holdover_led")
        self.horizontalLayout_4.addWidget(self.holdover_led)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_7 = QtWidgets.QLabel(self.gbTimebase)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.pllstatus_label = QtWidgets.QLabel(self.gbTimebase)
        self.pllstatus_label.setObjectName("pllstatus_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.pllstatus_label)
        self.label_8 = QtWidgets.QLabel(self.gbTimebase)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.duration_label = QtWidgets.QLabel(self.gbTimebase)
        self.duration_label.setObjectName("duration_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.duration_label)
        self.label_10 = QtWidgets.QLabel(self.gbTimebase)
        self.label_10.setObjectName("label_10")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.timeerr_label = QtWidgets.QLabel(self.gbTimebase)
        self.timeerr_label.setObjectName("timeerr_label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.timeerr_label)
        self.label_9 = QtWidgets.QLabel(self.gbTimebase)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.aveerr_label = QtWidgets.QLabel(self.gbTimebase)
        self.aveerr_label.setObjectName("aveerr_label")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.aveerr_label)
        self.label_11 = QtWidgets.QLabel(self.gbTimebase)
        self.label_11.setObjectName("label_11")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.freqcontrol_label = QtWidgets.QLabel(self.gbTimebase)
        self.freqcontrol_label.setObjectName("freqcontrol_label")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.freqcontrol_label)
        self.label_12 = QtWidgets.QLabel(self.gbTimebase)
        self.label_12.setObjectName("label_12")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.looptc_label = QtWidgets.QLabel(self.gbTimebase)
        self.looptc_label.setObjectName("looptc_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.looptc_label)
        self.verticalLayout_4.addLayout(self.formLayout)
        self.gridLayout.addWidget(self.gbTimebase, 2, 0, 1, 1)
        self.gbEvents = QtWidgets.QGroupBox(Form)
        self.gbEvents.setObjectName("gbEvents")
        self.formLayout_4 = QtWidgets.QFormLayout(self.gbEvents)
        self.formLayout_4.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_13 = QtWidgets.QLabel(self.gbEvents)
        self.label_13.setObjectName("label_13")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.event_count_label = QtWidgets.QLabel(self.gbEvents)
        self.event_count_label.setObjectName("event_count_label")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.event_count_label)
        self.label_14 = QtWidgets.QLabel(self.gbEvents)
        self.label_14.setObjectName("label_14")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_14)
        self.event_desc_label = QtWidgets.QLabel(self.gbEvents)
        self.event_desc_label.setObjectName("event_desc_label")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.event_desc_label)
        self.label_15 = QtWidgets.QLabel(self.gbEvents)
        self.label_15.setObjectName("label_15")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_15)
        self.event_date_label = QtWidgets.QLabel(self.gbEvents)
        self.event_date_label.setObjectName("event_date_label")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.event_date_label)
        self.label_16 = QtWidgets.QLabel(self.gbEvents)
        self.label_16.setObjectName("label_16")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_16)
        self.event_time_label = QtWidgets.QLabel(self.gbEvents)
        self.event_time_label.setObjectName("event_time_label")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.event_time_label)
        self.event_clear_btn = QtWidgets.QPushButton(self.gbEvents)
        self.event_clear_btn.setObjectName("event_clear_btn")
        self.formLayout_4.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.event_clear_btn)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_4.setItem(4, QtWidgets.QFormLayout.FieldRole, spacerItem1)
        self.gridLayout.addWidget(self.gbEvents, 2, 1, 1, 1)
        self.gbAlarms = QtWidgets.QGroupBox(Form)
        self.gbAlarms.setObjectName("gbAlarms")
        self.formLayout_5 = QtWidgets.QFormLayout(self.gbAlarms)
        self.formLayout_5.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_5.setRowWrapPolicy(QtWidgets.QFormLayout.DontWrapRows)
        self.formLayout_5.setObjectName("formLayout_5")
        self.label_17 = QtWidgets.QLabel(self.gbAlarms)
        self.label_17.setObjectName("label_17")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_17)
        self.alarm_status_label = QtWidgets.QLabel(self.gbAlarms)
        self.alarm_status_label.setObjectName("alarm_status_label")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.alarm_status_label)
        self.label_18 = QtWidgets.QLabel(self.gbAlarms)
        self.label_18.setObjectName("label_18")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_18)
        self.alarm_cause1_label = QtWidgets.QLabel(self.gbAlarms)
        self.alarm_cause1_label.setObjectName("alarm_cause1_label")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.alarm_cause1_label)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_5.setItem(4, QtWidgets.QFormLayout.FieldRole, spacerItem2)
        self.alarm_clear_btn = QtWidgets.QPushButton(self.gbAlarms)
        self.alarm_clear_btn.setObjectName("alarm_clear_btn")
        self.formLayout_5.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.alarm_clear_btn)
        self.alarm_cause2_label = QtWidgets.QLabel(self.gbAlarms)
        self.alarm_cause2_label.setText("")
        self.alarm_cause2_label.setObjectName("alarm_cause2_label")
        self.formLayout_5.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.alarm_cause2_label)
        self.alarm_cause3_label = QtWidgets.QLabel(self.gbAlarms)
        self.alarm_cause3_label.setText("")
        self.alarm_cause3_label.setObjectName("alarm_cause3_label")
        self.formLayout_5.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.alarm_cause3_label)
        self.gridLayout.addWidget(self.gbAlarms, 2, 2, 1, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setRowStretch(1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.restart_btn, self.event_clear_btn)
        Form.setTabOrder(self.event_clear_btn, self.alarm_clear_btn)
        Form.setTabOrder(self.alarm_clear_btn, self.notime_led)
        Form.setTabOrder(self.notime_led, self.antopen_led)
        Form.setTabOrder(self.antopen_led, self.antshort_led)
        Form.setTabOrder(self.antshort_led, self.nosat_led)
        Form.setTabOrder(self.nosat_led, self.utc_led)
        Form.setTabOrder(self.utc_led, self.survey_led)
        Form.setTabOrder(self.survey_led, self.leapsec_led)
        Form.setTabOrder(self.leapsec_led, self.legend_gps)
        Form.setTabOrder(self.legend_gps, self.legend_glonass)
        Form.setTabOrder(self.legend_glonass, self.legend_galileo)
        Form.setTabOrder(self.legend_galileo, self.locked_led)
        Form.setTabOrder(self.locked_led, self.stable_led)
        Form.setTabOrder(self.stable_led, self.holdover_led)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.gbUTC.setTitle(_translate("Form", "UTC"))
        self.labelUTC.setText(_translate("Form", "January 1, 1980  /  00:00:00"))
        self.gbWarnings.setTitle(_translate("Form", "Warnings"))
        self.notime_led.setText(_translate("Form", "No Time"))
        self.antopen_led.setText(_translate("Form", "Ant Open"))
        self.antshort_led.setText(_translate("Form", "Ant Short"))
        self.nosat_led.setText(_translate("Form", "No Satellites"))
        self.utc_led.setText(_translate("Form", "UTC Unknown"))
        self.survey_led.setText(_translate("Form", "Survey in Prog."))
        self.leapsec_led.setText(_translate("Form", "Leap Sec Pending"))
        self.gbPosition.setTitle(_translate("Form", "Position"))
        self.label.setText(_translate("Form", "Latitude:"))
        self.latitude_label.setText(_translate("Form", "0.000000 N"))
        self.label_2.setText(_translate("Form", "Longitude:"))
        self.longitude_label.setText(_translate("Form", "000.000000 W"))
        self.label_3.setText(_translate("Form", "Altitude:"))
        self.altitude_label.setText(_translate("Form", "0.00 m"))
        self.label_4.setText(_translate("Form", "Survey:"))
        self.restart_btn.setText(_translate("Form", "Restart"))
        self.gbSatellites.setTitle(_translate("Form", "Satellites"))
        self.label_5.setText(_translate("Form", "Tracking:"))
        self.tracking_label.setText(_translate("Form", "0"))
        self.label_6.setText(_translate("Form", "SNR:"))
        self.snr_label.setText(_translate("Form", "0"))
        self.legend_gps.setText(_translate("Form", "GPS"))
        self.legend_glonass.setText(_translate("Form", "GLONASS"))
        self.legend_galileo.setText(_translate("Form", "GALILEO"))
        self.legend_beidou.setText(_translate("Form", "BEIDOU"))
        self.gbTimebase.setTitle(_translate("Form", "Timebase"))
        self.locked_led.setText(_translate("Form", "Locked"))
        self.stable_led.setText(_translate("Form", "Stable"))
        self.holdover_led.setText(_translate("Form", "Holdover"))
        self.label_7.setText(_translate("Form", "PLL Status:"))
        self.pllstatus_label.setText(_translate("Form", "Warmup"))
        self.label_8.setText(_translate("Form", "Duration:"))
        self.duration_label.setText(_translate("Form", "0 s"))
        self.label_10.setText(_translate("Form", "Time Err:"))
        self.timeerr_label.setText(_translate("Form", "0 ns"))
        self.label_9.setText(_translate("Form", "Ave Err:"))
        self.aveerr_label.setText(_translate("Form", "0 ns"))
        self.label_11.setText(_translate("Form", "Freq ctrl:"))
        self.freqcontrol_label.setText(_translate("Form", "0.000000 V"))
        self.label_12.setText(_translate("Form", "Loop TC"))
        self.looptc_label.setText(_translate("Form", "250 s"))
        self.gbEvents.setTitle(_translate("Form", "Timebase Events"))
        self.label_13.setText(_translate("Form", "Count:"))
        self.event_count_label.setText(_translate("Form", "0"))
        self.label_14.setText(_translate("Form", "Event:"))
        self.event_desc_label.setText(_translate("Form", "Power on"))
        self.label_15.setText(_translate("Form", "Date:"))
        self.event_date_label.setText(_translate("Form", "1/1/1980"))
        self.label_16.setText(_translate("Form", "Time:"))
        self.event_time_label.setText(_translate("Form", "00:00:00"))
        self.event_clear_btn.setText(_translate("Form", "Clear"))
        self.gbAlarms.setTitle(_translate("Form", "Alarm Status"))
        self.label_17.setText(_translate("Form", "Status:"))
        self.alarm_status_label.setText(_translate("Form", "Inactive"))
        self.label_18.setText(_translate("Form", "Cause:"))
        self.alarm_cause1_label.setText(_translate("Form", "None"))
        self.alarm_clear_btn.setText(_translate("Form", "Clear"))

from satellites_widget import SatellitesWidget
from status_checkbox import StatusCheckBox
