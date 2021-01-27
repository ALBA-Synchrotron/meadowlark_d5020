# -*- coding: utf-8 -*-
#
# This file is part of the Meadowlark D5020 project
#
# Copyright (c) 2021 Alberto López Sánchez
# Distributed under the GNU General Public License v3. See LICENSE for more info.

"""Tango server class for Meadowlark_d5020"""

import serial
from serial.serialutil import SerialException
from tango import GreenMode
from tango import Attr
from tango.attr_data import AttrData
from tango.server import Device, attribute, command, device_property

from meadowlark_d5020.core import Meadowlark_d5020 as Core
from meadowlark_d5020.core import Channel
from meadowlark_d5020.core import Waveform


class Meadowlark_d5020(Device):

    serial_url = device_property(
        dtype=str, default_value="/tmp/meadowlark_d5020")

    porpe2l = device_property(
        dtype=str, default_value="/tmp/meadowlark_d5020")

    def init_device(self):
        super().init_device()
        try:
            self.connection = serial.serial_for_url("/tmp/meadowlark_d5020")
            self.meadowlark_d5020 = Core(self.connection)

            self.channels = [self.meadowlark_d5020.channels[0],
                             self.meadowlark_d5020.channels[1]]

            for c in range(0, len(self.channels)):
                print("Channel ", c)
                channel = self.channels[c]

                def get_waveform():
                    return channel.waveform

                def set_waveform(value):
                    channel.waveform = value

                self.add_attribute(
                    attribute(name="wavefrom" + str(c),
                              dtype=Waveform,
                              label="Waveform pattern"),
                    r_meth=get_waveform, w_meth=set_waveform)
        except SerialException as e:
            print("Serial Exception initializing device: ", e)
            print("\nCheck the properties!")
    ###########################################################################

    ###########################################################################

    @attribute(dtype=int, unit="mV", label="Channel1 V1", min_value=0,
               max_value=10000)
    def v1(self):
        return self.meadowlark_d5020.channel_1.v1

    @v1.setter
    def set_channel1_v1(self, value):
        self.meadowlark_d5020.channel_1.v1 = value

    @attribute(dtype=int, unit="mV", label="Channel2 V1", min_value=0,
               max_value=10000)
    def channel2_v1(self):
        return self.meadowlark_d5020.channel_2.v1

    @channel2_v1.setter
    def set_channel1_v1(self, value):
        self.meadowlark_d5020.channel_2.v1 = value

    ###########################################################################

    @attribute(dtype=int, unit="mV", label="V2", min_value=0, max_value=10000,
               doc="v2")
    def v2(self):
        return self.meadowlark_d5020.v2

    @v2.setter
    def set_v2(self, value):
        self.meadowlark_d5020.v2 = value

    ###########################################################################

    @attribute(dtype=int, unit="ms", label="period", min_value=0,
               max_value=65535, doc="period")
    def period(self):
        return self.meadowlark_d5020.period

    @period.setter
    def set_period(self, value):
        self.meadowlark_d5020.period = value

    ###########################################################################

    @attribute(dtype=int, unit="degrees", label="phase", min_value=-360,
               max_value=360, doc="phase")
    def phase(self):
        return self.meadowlark_d5020.phase

    @phase.setter
    def set_phase(self, value):
        self.meadowlark_d5020.phase = value

    ###########################################################################

    @attribute(dtype=int, unit="%", label="duty cycle", min_value=0,
               max_value=100, doc="duty cycle")
    def duty_cycle(self):
        return self.meadowlark_d5020.duty_cycle

    @duty_cycle.setter
    def set_duty_cycle(self, value):
        self.meadowlark_d5020.duty_cycle = value

    ###########################################################################

    @attribute(dtype=int, unit="mV", label="Transient Nematic Effect Voltage",
               min_value=0, max_value=10000, doc="T.N.E Voltage")
    def tne_voltage(self):
        return self.meadowlark_d5020.tne_voltage

    @tne_voltage.setter
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

    @command
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
