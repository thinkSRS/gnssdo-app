# Copyright: Stanford Reserach Systems, Inc and contributors
# License: GNU GPL, version 3 or later; https://www.gnu.org/licenses/gpl-3.0.html
import math
from error import GpsdoError


class SatInfo:
    pass


class Gpsdo:
    def __init__(self, serial_port):
        self.serial_port = serial_port
        self.timeout = 3000
        self.model = "FS752"
        self.version = 0.50

    def isOldFS740(self):
        return "FS740" == self.model and self.version < 4.00

    def read_bytes(self, cnt):
        cnt_read = 0
        result = b""
        while cnt_read < cnt:
            available = self.serial_port.bytesAvailable()
            if available or self.serial_port.waitForReadyRead(self.timeout):
                this_result = self.serial_port.read(cnt - cnt_read)
                result += this_result
                cnt_read += len(this_result)
            else:
                raise GpsdoError("Read timeout")
        return result

    def write_bytes(self, data):
        self.serial_port.write(data)

    def write(self, cmd):
        cmd += "\n"
        self.write_bytes(cmd.encode())

    def read(self):
        result = b""
        this_result = self.read_bytes(1)
        while this_result != b"\n":
            result += this_result
            this_result = self.read_bytes(1)
        str_result = result.decode()
        return str_result.strip()

    def get_serial_model_and_version(self):
        self.write("*IDN?")
        id_str = self.read().strip()
        company, model, serial, version = id_str.split(",")
        version = version[3:]
        self.serial = serial
        self.model = model
        self.version = float(version[0:4])
        return serial, model, version

    def get_options(self):
        self.write("*OPT?")
        str_options = self.read().strip()
        return str_options.split(",")

    def set_timeout(self, value):
        self.timeout = value

    def get_position(self):
        self.write("GPS:POS?")
        ans = self.read()
        results = ans.split(",")
        results = [float(v) for v in results]
        results[0] *= 180.0/math.pi
        results[1] *= 180.0/math.pi
        return results

    def get_survey_progress(self):
        self.write("GPS:POS:SURV:PROG?")
        return int(self.read())

    def get_ques_status(self):
        self.write("STAT:QUES:COND?")
        return int(self.read())

    def get_gps_model_and_version(self):
        if self.isOldFS740():
            version = '""'
            model = '""'
        else:
            self.write("GPS:VERS?")
            ver_str = self.read().strip()
            version, model = ver_str.split(",")
        # Remove quotes
        version = version[1:-1]
        model = model[1:-1]
        return model, version

    def get_gps_status(self):
        self.write("STAT:GPS:COND?")
        return int(self.read())

    def get_timebase_state(self):
        self.write("TBAS:STAT?")
        return self.read().strip()

    def get_loop_time_constant(self):
        self.write("TBAS:TCON?")
        return int(self.read())

    def get_warmup_duration(self):
        self.write("TBAS:WARM?")
        return int(self.read())

    def get_lock_duration(self):
        self.write("TBAS:LOCK?")
        return int(self.read())

    def get_holdover_duration(self):
        self.write("TBAS:HOLD?")
        return int(self.read())

    def get_timebase_time_interval(self):
        self.write("TBAS:TINT?")
        return float(self.read())

    def get_timebase_average_time_interval(self):
        self.write("TBAS:TINT? AVER")
        return float(self.read())

    def get_efc(self):
        self.write("TBAS:FCON?")
        return float(self.read())

    def get_event_count(self):
        self.write("TBAS:EVENT:COUNT?")
        return int(self.read())

    def get_event(self):
        self.write("TBAS:EVENT?")
        return self.extract_event()

    def peek_event(self):
        if self.isOldFS740():
            event = ["INV",2000,1,1,0,0,0]
        else:
            self.write("TBAS:EVENT:PEEK?")
            event = self.extract_event()
        return event

    def extract_event(self):
        result = self.read().strip()
        result_list = result.split(",")
        event_list = [result_list[0]]
        event_list.extend([int(v) for v in result_list[1:]])
        return event_list

    def get_alarm(self):
        self.write("SYST:ALAR?")
        return int(self.read())

    def get_alarm_mode(self):
        self.write("SYST:ALAR:MOD?")
        return self.read().strip()

    def get_alarm_condition(self):
        self.write("SYST:ALAR:COND?")
        return int(self.read())

    def get_alarm_event(self):
        self.write("SYST:ALAR:EVENT?")
        return int(self.read())

    def get_alarm_holdover_duration(self):
        self.write("SYST:ALAR:DUR?")
        return int(float(self.read()))

    def get_alarm_offset_limit(self):
        self.write("SYST:ALAR:TINT?")
        return float(self.read())

    def get_alarm_enable(self):
        self.write("SYST:ALAR:ENAB?")
        return int(self.read())

    def get_pulse_offset(self):
        if "FS740" == self.model:
            self.write("SOUR3:PHAS:SYNC:TDEL?")
        else:
            self.write("SOUR:PHAS:SYNC:TDEL?")
        return float(self.read())

    def get_used_satellites(self):
        self.write("GPS:SAT:USE?")
        ans = self.read()
        results = ans.split(",")
        event = [results[0]]
        event.extend([int(v) for v in results[1:]])
        results = [int(v) for v in results]
        if results[0] == (len(results) - 1):
            results = results[1:]
        else:
            results = []
        return results

    def get_sat_info(self):
        self.write("GPS:SAT:TRAC:STAT?")
        results = [int(item) for item in self.read().split(",")]
        count = len(results) // 8
        info_list = []
        for i in range(count):
            index = 8 * i
            sat_info = SatInfo()
            sat_info.sv_number = results[index]
            sat_info.used = results[index+1]
            sat_info.ephemeris = results[index+2]
            sat_info.snr = results[index+4]
            sat_info.elevation = results[index+5]
            sat_info.azimuth = results[index+6]
            info_list.append(sat_info)
        return info_list

    def get_snr(self):
        if self.isOldFS740():
            snr = 0
        else:
            self.write("GPS:SAT:SNR?")
            snr = int(self.read())
        return snr

    def get_date_and_time(self):
        tm = [0, 0, 0]
        dt = [-1, -1, -1]
        self.write("SYST:DATE?")
        dt2 = [int(item) for item in self.read().split(",")]
        while dt2 != dt:
            dt = dt2
            self.write("SYST:TIME?")
            tm = [float(item) for item in self.read().split(",")]
            tm[0] = int(tm[0])
            tm[1] = int(tm[1])
            self.write("SYST:DATE?")
            dt2 = [int(item) for item in self.read().split(",")]
        dt.extend(tm)
        return dt

    def get_lock_gnss(self):
        self.write("TBAS:CONF:LOCK?")
        return int(self.read())

    def get_loop_bandwidth(self):
        self.write("TBAS:CONF:BWID?")
        return self.read().strip()

    def get_holdover_mode(self):
        self.write("TBAS:CONF:HMOD?")
        return self.read().strip()

    def get_holdover_limit(self):
        self.write("TBAS:CONF:LIM?")
        return float(self.read())

    def get_manual_time_constant(self):
        self.write("TBAS:TCON? MAN")
        return int(self.read())

    def get_constellation(self):
        if self.isOldFS740():
            constellation = 1
        else:
            self.write("GPS:CONF:CONS?")
            constellation = int(self.read())
        return constellation

    def get_time_alignment(self):
        self.write("GPS:CONF:ALIG?")
        return self.read().strip()

    def get_timing_quality(self):
        self.write("GPS:CONF:QUAL?")
        return self.read().strip()

    def get_min_snr(self):
        self.write("GPS:CONF:MODE?")
        antijamming, min_elevation, min_snr = self.read().split(",")
        return float(min_snr)

    def get_min_elevation(self):
        self.write("GPS:CONF:MODE?")
        antijamming, min_elevation, min_snr = self.read().split(",")
        return float(min_elevation) * 180.0 / math.pi

    def get_survey_mode(self):
        self.write("GPS:CONF:SURV?")
        return self.read().strip()

    def get_survey_fixes(self):
        self.write("GPS:CONF:SURV:FIX?")
        return int(self.read())

    def get_antenna_delay(self):
        self.write("GPS:CONF:ADEL?")
        return float(self.read())

    def get_local_time_offset(self):
        self.write("SYST:TIM:LOFF?")
        return int(self.read())
