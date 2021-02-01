# -*- coding: utf-8 -*-
#
# This file is part of the Meadowlark D5020 project
#
# Copyright (c) 2021 Alberto López Sánchez
# Distributed under the GNU General Public License v3. See LICENSE for more info.

"""Tango server class for Meadowlark_d5020"""

import serial
from tango.server import Device, attribute, command, device_property

from meadowlark_d5020.core import Meadowlark_d5020 as D5020
from meadowlark_d5020.core import Waveform


class Meadowlark_d5020(Device):

    url = device_property(dtype=str)
    channel = device_property(dtype=int)

    def init_device(self):
        super().init_device()
        conn = serial.serial_for_url(self.url)
        self.meadowlark_d5020 = D5020(self.channel, conn)

    ###########################################################################

    @attribute(dtype=Waveform, label="Waveform pattern")
    def waveform(self):
        return self.meadowlark_d5020.waveform

    @waveform.setter
    def set_waveform(self, value):
        self.meadowlark_d5020.waveform = value

    ###########################################################################

    @attribute(dtype=int, unit="mV", label="V1", min_value=D5020.MIN_VOLTAGE, 
            max_value=D5020.MAX_VOLTAGE, doc="v1")
    def v1(self):
        return self.meadowlark_d5020.v1

    @v1.setter
    def set_v1(self, value):
        self.meadowlark_d5020.v1 = value

    ###########################################################################

    @attribute(dtype=int, unit="mV", label="V2", min_value=D5020.MIN_VOLTAGE, 
               max_value=D5020.MAX_VOLTAGE, doc="v2")
    def v2(self):
        return self.meadowlark_d5020.v2

    @v2.setter
    def set_v2(self, value):
        self.meadowlark_d5020.v2 = value

    ###########################################################################

    @attribute(dtype=int, unit="ms", label="period", min_value=D5020.MIN_PERIOD,
               max_value=D5020.MAX_PERIOD, doc="period")
    def period(self):
        return self.meadowlark_d5020.period

    @period.setter
    def set_period(self, value):
        self.meadowlark_d5020.period = value

    ###########################################################################

    @attribute(dtype=int, unit="degrees", label="phase", 
               min_value=-D5020.MAX_PHASE, max_value=D5020.MAX_PHASE, 
               doc="phase")
    def phase(self):
        return self.meadowlark_d5020.phase

    @phase.setter
    def set_phase(self, value):
        self.meadowlark_d5020.phase = value

    ###########################################################################

    @attribute(dtype=int, unit="%", label="duty cycle", 
               min_value=D5020.MIN_DUTY_CICLE, max_value=D5020.MAX_DUTY_CICLE,
               doc="duty cycle")
    def duty_cycle(self):
        return self.meadowlark_d5020.duty_cycle

    @duty_cycle.setter
    def set_duty_cycle(self, value):
        self.meadowlark_d5020.duty_cycle = value

    ###########################################################################

    @attribute(dtype=int, unit="mV", label="Transient Nematic Effect Voltage",
               min_value=D5020.MIN_VOLTAGE, 
               max_value=D5020.MAX_VOLTAGE, doc="T.N.E Voltage")
    def tne_voltage(self):
        return self.meadowlark_d5020.tne_voltage

    @tne_voltage.setter
    def set_tne_voltage(self, value):
        self.meadowlark_d5020.tne_voltage = value

    ###########################################################################

    @attribute(dtype=int, unit="ms", label="Transient Nematic Effect Time",
               min_value=D5020.MIN_TNE_TIME, max_value=D5020.MAX_TNE_TIME, 
               doc="T.N.E Time")
    def tne_time(self):
        return self.meadowlark_d5020.tne_time

    @tne_time.setter
    def set_tne_time(self, value):
        self.meadowlark_d5020.tne_time = value

    ###########################################################################

    @attribute(dtype=bool, unit="ºC", label="LC Temperature",
               doc="Query current temperature of temperature controlled LC on "
               "channel n.")
    def lc_temperature(self):
        return self.meadowlark_d5020.lc_temperature()

    ###########################################################################

    @attribute(dtype=float, unit="ºC", label="Temperature Setpoint",
               min_value=0.0, max_value=226.0)
    def temperature_setpoint(self):
        return self.meadowlark_d5020.temperature_setpoint()

    @temperature_setpoint.setter
    def set_temperature_setpoint(self, value):
        self.meadowlark_d5020.temperature_setpoint = value

    ###########################################################################

if __name__ == "__main__":
    import logging
    fmt = "%(asctime)s %(levelname)s %(name)s %(message)s"
    logging.basicConfig(level="DEBUG", format=fmt)
    Meadowlark_d5020.run_server()
