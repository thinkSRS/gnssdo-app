# Copyright: Stanford Reserach Systems, Inc and contributors
# License: GNU GPL, version 3 or later; https://www.gnu.org/licenses/gpl-3.0.html
import time
from enum import Enum, unique

from PyQt5.QtCore import (QObject, QMutex, QCoreApplication, pyqtSignal)
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

import device
from error import GpsdoError


@unique
class ModeEnum(Enum):
    MODE_STATUS = 0
    MODE_SETUP = 1
    MODE_CONSOLE = 2
    MODE_QUIT = 3


class GpsdoData:
    pass


class GpsdoSetup:
    pass


class CommThread(QObject):
    error_signal = pyqtSignal(Exception)
    data_signal = pyqtSignal(GpsdoData)
    setup_signal = pyqtSignal(GpsdoSetup)
    disconnect_signal = pyqtSignal()
    receive_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.serial_port = None
        self.gps = None
        self.mutex = QMutex(QMutex.Recursive)
        # Mutex protected variables
        self.connected = False
        self.port_name = None
        self.mode = ModeEnum.MODE_STATUS

    def emit_error(self, err):
        self.error_signal.emit(err)

    def emit_data(self, data):
        self.data_signal.emit(data)

    def emit_setup(self, setup):
        self.setup_signal.emit(setup)

    def emit_receive_data(self, text):
        self.receive_signal.emit(text)

    def is_connected(self):
        self.mutex.lock()
        result = self.connected
        self.mutex.unlock()
        return result

    def connect(self, new_state):
        self.mutex.lock()
        self.connected = new_state
        self.mutex.unlock()

    def set_serial_port(self, port_name):
        self.mutex.lock()
        self.port_name = port_name
        self.mutex.unlock()

    def set_mode(self, mode):
        self.mutex.lock()
        self.mode = mode
        self.mutex.unlock()

    def get_mode(self):
        self.mutex.lock()
        result = self.mode
        self.mutex.unlock()
        return result

    def connect_to_serial_port(self):
        port = self.find_serial_port()
        self.serial_port = QSerialPort(port)
        # Try to open the port
        if self.serial_port.open(QSerialPort.ReadWrite):
            self.serial_port.setBaudRate(115200, QSerialPort.AllDirections)
            self.serial_port.setParity(QSerialPort.NoParity)
            self.serial_port.setDataBits(QSerialPort.Data8)
            self.serial_port.setStopBits(QSerialPort.OneStop)
            self.serial_port.setFlowControl(QSerialPort.HardwareControl)
        else:
            self.serial_port = None
            raise GpsdoError("Error opening " + self.port_name)

    def find_serial_port(self):
        for port in QSerialPortInfo.availablePorts():
            if port.portName() == self.port_name:
                the_port = port
                break
        else:
            raise GpsdoError(self.port_name + " not found!")
        return the_port

    def disconnect_from_serial_port(self):
        if self.serial_port:
            self.serial_port.close()
            self.serial_port = None

    def work(self):
        while self.get_mode() != ModeEnum.MODE_QUIT:
            start_time = time.time()
            if self.is_connected():
                try:
                    try:
                        self.connect_to_serial_port()
                        self.gps = device.Gpsdo(self.serial_port)
                        while self.get_mode() != ModeEnum.MODE_QUIT and self.is_connected():
                            self.do_worker_loop()
                            QCoreApplication.processEvents()
                    except Exception as err:
                        self.emit_error(err)
                finally:
                    self.disconnect_from_serial_port()
                    self.connect(False)
                    self.gps = None
                    self.disconnect_signal.emit()
            QCoreApplication.processEvents()

            # run at a maximum of 10Hz
            stop_time = start_time + 0.100
            wait_time = max(stop_time - time.time(), 0)
            time.sleep(wait_time)

    def do_worker_loop(self):
        mode = self.get_mode()
        if ModeEnum.MODE_STATUS == mode:
            self.do_status_loop()
        elif ModeEnum.MODE_CONSOLE == mode:
            self.do_console_loop()
        elif ModeEnum.MODE_SETUP == mode:
            self.do_setup_loop()

    def do_status_loop(self):
        data = GpsdoData()
        data.serial, data.model, data.version = self.gps.get_serial_model_and_version()
        data.position = self.gps.get_position()
        data.survey = self.gps.get_survey_progress()
        data.satellites = self.gps.get_used_satellites()
        data.satellite_info = self.gps.get_sat_info()
        data.snr = self.gps.get_snr()
        data.time_alignment = self.gps.get_time_alignment()
        data.local_time_offset = self.gps.get_local_time_offset()
        data.time = self.gps.get_date_and_time()
        data.gps_status = self.gps.get_gps_status()
        data.ques_status = self.gps.get_ques_status()
        data.timebase_state = self.gps.get_timebase_state()
        data.loop_tc = self.gps.get_loop_time_constant()
        data.warmup_duration = self.gps.get_warmup_duration()
        data.lock_duration = self.gps.get_lock_duration()
        data.holdover_duration = self.gps.get_holdover_duration()
        if "LOCK" == data.timebase_state or "MAN" == data.timebase_state or "NGPS" == data.timebase_state or \
                "BGPS" == data.timebase_state:
            data.time_err = self.gps.get_timebase_time_interval()
            data.average_err = self.gps.get_timebase_average_time_interval()
        else:
            data.time_err = 0.0
            data.average_err = 0.0
        data.freq_control = self.gps.get_efc()
        data.event_count = self.gps.get_event_count()
        data.event = self.gps.peek_event()
        data.alarm = self.gps.get_alarm()
        data.alarm_mode = self.gps.get_alarm_mode()
        data.alarm_condition = self.gps.get_alarm_condition()
        data.alarm_event = self.gps.get_alarm_event()
        self.emit_data(data)

    def do_setup_loop(self):
        setup = GpsdoSetup()
        setup.serial, setup.model, setup.version = self.gps.get_serial_model_and_version()
        setup.options = self.gps.get_options()
        setup.constellation = self.gps.get_constellation()
        setup.lock_gnss = self.gps.get_lock_gnss()
        setup.bandwidth = self.gps.get_loop_bandwidth()
        setup.manual_time_constant = self.gps.get_manual_time_constant()
        setup.holdover_mode = self.gps.get_holdover_mode()
        setup.holdover_limit = self.gps.get_holdover_limit()
        setup.gps_model, setup.gps_version = self.gps.get_gps_model_and_version()
        setup.time_alignment = self.gps.get_time_alignment()
        setup.time_quality = self.gps.get_timing_quality()
        setup.min_snr = self.gps.get_min_snr()
        setup.min_elevation = self.gps.get_min_elevation()
        setup.local_time_offset = self.gps.get_local_time_offset()
        setup.survey_mode = self.gps.get_survey_mode()
        setup.survey_fixes = self.gps.get_survey_fixes()
        setup.antenna_delay = self.gps.get_antenna_delay()
        setup.alarm_mode = self.gps.get_alarm_mode()
        setup.alarm_holdover_duration = self.gps.get_alarm_holdover_duration()
        setup.alarm_offset_limit = self.gps.get_alarm_offset_limit()
        setup.alarm_enable = self.gps.get_alarm_enable()
        setup.pulse_offset = self.gps.get_pulse_offset()
        self.emit_setup(setup)

    def do_console_loop(self):
        available = self.gps.serial_port.bytesAvailable()
        if available:
            raw_bytes = self.gps.read_bytes(available)
            text = raw_bytes.decode()
            self.emit_receive_data(text)

    def send_command(self, text):
        if self.is_connected():
            self.gps.write(text)
