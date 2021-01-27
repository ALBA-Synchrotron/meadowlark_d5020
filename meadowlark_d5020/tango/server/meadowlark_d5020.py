# -*- coding: utf-8 -*-
#
# This file is part of the Meadowlark D5020 project
#
# Copyright (c) 2021 Alberto López Sánchez
# Distributed under the GNU General Public License v3. See LICENSE for more info.

"""Tango server class for Meadowlark_d5020"""

import serial
from tango import GreenMode
from tango.server import Device, attribute, command, device_property

from meadowlark_d5020.core import Meadowlark_d5020 as Core
from meadowlark_d5020.core import Channel
from meadowlark_d5020.core import Waveform


class Meadowlark_d5020(Device):

    url = device_property(dtype=str)

    def init_device(self):
        super().init_device()
        self.connection = serial.serial_for_url(self.url)
        self.meadowlark_d5020 = Core(self.connection)

    ###########################################################################

    @attribute(dtype=Waveform, label="Waveform pattern")
    def channel1_waveform(self):
        return self.meadowlark_d5020.channel_1.waveform

    @channel1_waveform.setter
    def channel1_set_waveform(self, value):
        self.meadowlark_d5020.channel_1.waveform = value

    ###########################################################################

    @attribute(dtype=int, unit="mV", label="V1", min_value=0, max_value=10000,
               doc="v1")
    def channel1_v1(self):
        return self.meadowlark_d5020.channel_1.v1

    @channel1_v1.setter
    def set_v1(self, value):
        self.meadowlark_d5020.channel_1.v1 = value

    ###########################################################################

    @attribute(dtype=int, unit="mV", label="V2", min_value=0, max_value=10000,
               doc="v2")
    def channel1_v2(self):
        return self.meadowlark_d5020.channel_1.v2

    @channel1_v2.setter
    def set_v2(self, value):
        self.meadowlark_d5020.channel_1.v2 = value

    ###########################################################################

    @attribute(dtype=int, unit="ms", label="period", min_value=0,
               max_value=65535, doc="period")
    def channel1_period(self):
        return self.meadowlark_d5020.channel_1.period

    @channel1_period.setter
    def channel1_set_period(self, value):
        self.meadowlark_d5020.channel_1.period = value

    ###########################################################################

    @attribute(dtype=int, unit="degrees", label="phase", min_value=-360,
               max_value=360, doc="phase")
    def channel1_phase(self):
        return self.meadowlark_d5020.channel_1.phase

    @channel1_phase.setter
    def channel1_set_phase(self, value):
        self.meadowlark_d5020.channel_1.phase = value

    ###########################################################################

    @attribute(dtype=int, unit="%", label="duty cycle", min_value=0,
               max_value=100, doc="duty cycle")
    def channel_1_duty_cycle(self):
        return self.meadowlark_d5020.duty_cycle

    @channel_1_duty_cycle.setter
    def channel_1_set_duty_cycle(self, value):
        self.meadowlark_d5020.channel_1.duty_cycle = value

    ###########################################################################

    @attribute(dtype=int, unit="mV", label="Transient Nematic Effect Voltage",
               min_value=0, max_value=10000, doc="T.N.E Voltage")
    def channel_1_tne_voltage(self):
        return self.meadowlark_d5020.channel_1.tne_voltage

    @channel_1tne_voltage.setter
    def set_tne_voltage(self, value):
        self.meadowlark_d5020.tne_voltage = value

    ###########################################################################

    @attribute(dtype=bool, label="External input",
               doc="Check if the external input is enabled")
    def external_input(self):
        return self.meadowlark_d5020.external_input

    @command
    def toggle_external_input(self):
        self.meadowlark_d5020.toggle_external_input()

    ###########################################################################

    @command
    def threshold(self, v1, v2):
        return self.meadowlark_d5020.threshold(v1, v2)

    ###########################################################################

    @attribute(dtype=bool, unit="ºC", label="LC Temperature",
               doc="Query current temperature of temperature controlled LC on "
               "channel n.")
    def lc_temperature(self):
        return self.meadowlark_d5020.lc_temperature()

    ###########################################################################

    @command()
    def trigger(self):
        return self.meadowlark_d5020.trigger()

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
